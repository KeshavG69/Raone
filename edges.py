from settings import TOTAL_MESSAGES_SUMMARY_TRIGGER
from langgraph.graph import END


def should_summarize_conversation(state):
    messages = state["messages"]

    if len(messages) > TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"

    return END


def select_workflow(state):
    workflow = state["workflow"]

    if workflow == "image":
        return "image_node"

    elif workflow == "audio":
        return "audio_node"

    else:
        return "conversation_node"
