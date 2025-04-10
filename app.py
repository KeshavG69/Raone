
from graph import create_workflow_graph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import  HumanMessage
import asyncio
checkpointer = MemorySaver()


graph_app=create_workflow_graph().compile(checkpointer=checkpointer)

query="what are u doing send photo"


config = {"configurable": {"thread_id": "1"}}
async def stream_response(content):
    async for chunk in graph_app.astream(
        {"messages": [HumanMessage(content=content)]},
        config

    ):
        print(chunk)


asyncio.run(stream_response(query))
output_state = asyncio.run(graph_app.aget_state(config={"configurable": {"thread_id": '1'}}))
print(output_state)
