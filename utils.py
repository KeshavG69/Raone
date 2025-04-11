import os
from langchain_groq import ChatGroq
import base64
from langchain_together import ChatTogether
from typing_extensions import Optional
from langchain_pinecone import PineconeVectorStore
from langchain_cohere import CohereEmbeddings
from together import Together
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()


def get_chat_model(temp=0.2):

  return ChatTogether(
      model='meta-llama/Llama-3.3-70B-Instruct-Turbo',
      temperature=temp,
      api_key=os.getenv('TOGETHER_504')
    )


def get_embedding_model():
  return CohereEmbeddings(
    model="embed-english-v3.0",
    cohere_api_key=os.getenv('COHERE_API_KEY')
)

def get_memory_llm(temp=0.2):
  return ChatGroq(
    model='gemma2-9b-it',
    temperature=temp,
    api_key=os.getenv('GROQ_API_KEY')
  )

def get_image_llm(temp=0.2):
  return ChatGroq(
    model='llama-3.2-90b-vision-preview',
    temperature=temp,
    api_key=os.getenv('GROQ_API_KEY')
  )

def get_create_image_model(temp=0.2):
  return Together(api_key=os.getenv('TOGETHER_504'))


def get_vector_store(INDEX_NAME='long-term-memory'):
  pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
  index_name = INDEX_NAME
  existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
  if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


  index = pc.Index(index_name)
  embeddings=get_embedding_model()
  return  PineconeVectorStore(index=index, embedding=embeddings)


async def analyze_image(image_data,prompt="Please describe what you see in this image in detail."):
    if isinstance(image_data, str):
        if not os.path.exists(image_data):
            raise ValueError(f"Image file not found: {image_data}")
        with open(image_data, "rb") as f:
            image_bytes = f.read()
    else:
       image_bytes = image_data
    
    if not image_bytes:
        raise ValueError("Image data cannot be empty")
    base64_image = base64.b64encode(image_bytes).decode("utf-8")


    messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                        },
                    ],
                }
            ]
    
    image_llm=get_image_llm()
    description=image_llm.invoke(messages)
    return description.content







  