from langchain_groq import ChatGroq
from zoneinfo import ZoneInfo
import asyncio
from langgraph.graph import MessagesState,END,START,StateGraph,add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from langchain_core.documents import Document
import uuid
import asyncio
import time
from uuid import uuid4
import os
import base64
from langgraph.checkpoint.memory import MemorySaver
import tempfile
from typing_extensions import Literal,Optional,Annotated,List
from datetime import datetime
from pinecone import Pinecone, ServerlessSpec
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage,AnyMessage
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
import operator
from groq import Groq
from together import Together
from elevenlabs import ElevenLabs, Voice, VoiceSettings

from state import AICompanionState
from schedhule import *
from settings import *
from prompt import *
from schedhule_manager import ScheduleContextGenerator
from text_to_speech import TextToSpeech
from utils import get_chat_model,get_create_image_model,get_vector_store









class RouterResponse(BaseModel):
    response_type: str = Field(
        description="The response type to give to the user. It must be one of: 'conversation', 'image' or 'audio'"
    )

class ExtractResponse(BaseModel):
  is_important:str=Field('Given a user message u have to tell if the message contains important message which can be stored The answer should be "true" or "false" ')
  formatted_memory:Optional[str]=Field('A formatted version of the user message which has facts which can be stored ')



class ScenarioPrompt(BaseModel):
    """Class for the scenario response"""

    narrative: str = Field(..., description="The AI's narrative response to the question")
    image_prompt: str = Field(..., description="The visual prompt to generate an image representing the scene")

async def memory_extraction_node(state: AICompanionState):
  """Extract and store important information from the last message."""

  if not state["messages"]:
    return {}

  prompt = MEMORY_ANALYSIS_PROMPT.format(message=state["messages"][-1])
  vector_store=get_vector_store()

  extract_llm=get_chat_model(temp=0.2).with_structured_output(ExtractResponse)
  analysis= await extract_llm.ainvoke(prompt)
#   print('memory_extraction_node'.upper())
#   print('OUTPUT')
#   print(analysis)
  if analysis.is_important and analysis.formatted_memory:
    results = vector_store.similarity_search_with_score(query=analysis.formatted_memory,k=1)

    if results:
    #   print(results[0][1])
      if results[0][1]>= SIMILARITY_THRESHOLD:
        return {}
    await vector_store.aadd_documents(documents=[Document(page_content=analysis.formatted_memory,metadata={"timestamp": datetime.now().isoformat()})])
  return {}


def get_router_chain():
    model = get_chat_model(temp=0.3).with_structured_output(RouterResponse)

    prompt = ChatPromptTemplate.from_messages(
        [("system", ROUTER_PROMPT), MessagesPlaceholder(variable_name="messages")]
    )

    return prompt | model

async def router_node(state: AICompanionState):
    chain = get_router_chain()
    response = await chain.ainvoke({"messages": state["messages"][-ROUTER_MESSAGES_TO_ANALYZE :]})
    return {"workflow": response.response_type}

def context_injection_node(state: AICompanionState):
  """
  Gets RaOne current Schedhule and injects it into the character card.

  """
  schedule_context = ScheduleContextGenerator.get_current_activity()
  if schedule_context != state.get("current_activity", ""):
      apply_activity = True
  else:
      apply_activity = False
  return {"apply_activity": apply_activity, "current_activity": schedule_context}


def memory_injection_node(state: AICompanionState):
  """Retrieve and inject relevant memories into the character card."""
  vector_store = get_vector_store()
  retriever= vector_store.as_retriever(search_kwargs={"k": MEMORY_TOP_K})

  # Get relevant memories based on recent conversation
  recent_context = " ".join([m.content for m in state["messages"][-3:]])
#   print('recent_context'.upper())
#   print(recent_context)
  memories = retriever.invoke(recent_context)
  memory_context=""
  if memories:
    memory_context="\n".join(f"- {memory.page_content}" for memory in memories)

  return {"memory_context": memory_context}

def get_character_response_chain(summary: str = ""):
    model = get_chat_model()
    system_message = CHARACTER_CARD_PROMPT

    if summary:
        system_message += f"\n\nSummary of conversation earlier between Ra.One and the user: {summary}"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt | model | StrOutputParser()


async def conversation_node(state: AICompanionState, config):
    current_activity = ScheduleContextGenerator.get_current_activity()
    # print('Messages'.upper())
    # print(state['messages'])
    memory_context = state.get("memory_context", "")

    chain = get_character_response_chain(state.get("summary", ""))

    response = await chain.ainvoke(
        {
            "messages": state["messages"],
            "current_activity": current_activity,
            "memory_context": memory_context,
        },
        config,
    )

    return {"messages": AIMessage(content=response)}


async def audio_node(state,config):

  current_activity = ScheduleContextGenerator.get_current_activity()
#   print('Messages'.upper())
#   print(state['messages'])
  memory_context = state.get("memory_context", "")
  chain = get_character_response_chain(state.get("summary", ""))
  tts=TextToSpeech()
  response = await chain.ainvoke(
      {
          "messages": state["messages"],
          "current_activity": current_activity,
          "memory_context": memory_context,
      },
      config,
  )
  output_audio = await tts.synthesize(response)
  return {"messages": response,"audio_buffer": output_audio}


async def image_node(state: AICompanionState, config):
  current_activity = ScheduleContextGenerator.get_current_activity()
  memory_context = state.get("memory_context", "")
  chain = get_character_response_chain(state.get("summary", ""))
  model=get_chat_model()
  image_create=get_create_image_model()
  formatted_history = "\n".join([f"{msg.type.title()}: {msg.content}" for msg in state["messages"][-5:]])
  scenario_structured_llm = model.with_structured_output(ScenarioPrompt)
  scenario_chain = (ChatPromptTemplate.from_template(

                    IMAGE_SCENARIO_PROMPT,
                )
                | scenario_structured_llm
            )
  scenario = await scenario_chain.ainvoke({"chat_history": formatted_history})
  os.makedirs("generated_images", exist_ok=True)
  img_path = f"generated_images/image_{str(uuid4())}.png"
  response=image_create.images.generate(
                prompt=scenario.image_prompt,
                model="black-forest-labs/FLUX.1-schnell-Free",
                width=1024,
                height=768,
                steps=4,
                n=1,
                response_format="b64_json",
            )
  image_data = base64.b64decode(response.data[0].b64_json)
  os.makedirs(os.path.dirname(img_path), exist_ok=True)
  with open(img_path, "wb") as f:
    f.write(image_data)
  scenario_message = HumanMessage(content=f"<image attached by Ra.One generated from prompt: {scenario.image_prompt}>")
  updated_messages = state["messages"] + [scenario_message]
  response = await chain.ainvoke(
        {
            "messages": updated_messages,
            "current_activity": current_activity,
            "memory_context": memory_context,
        },
        config,
    )

  return {"messages": AIMessage(content=response), "image_path": img_path}


async def summarize_conversation_node(state: AICompanionState):
  model = get_chat_model()
  summary = state.get("summary", "")

  if summary:
      summary_message = (
          f"This is summary of the conversation to date between Ra.One and the user: {summary}\n\n"
          "Extend the summary by taking into account the new messages above:"
      )
  else:
      summary_message = (
          "Create a summary of the conversation above between Ra.One and the user. "
          "The summary must be a short description of the conversation so far, "
          "but that captures all the relevant information shared between Ra.One and the user:"
      )

  messages = state["messages"] + [HumanMessage(content=summary_message)]
  response = await model.ainvoke(messages)

  delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][: TOTAL_MESSAGES_AFTER_SUMMARY]]
  return {"summary": response.content, "messages": delete_messages}




