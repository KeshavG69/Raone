import os
from io import BytesIO
from typing import Dict
import logging
import httpx
from fastapi import APIRouter, Request, Response
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from graph import create_workflow_graph
from utils import analyze_image
from speech_to_text import SpeechToText
from text_to_speech import TextToSpeech
from dotenv import load_dotenv


from settings import *

load_dotenv()
checkpointer = MemorySaver()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



speech_to_text = SpeechToText()
text_to_speech = TextToSpeech()

whatsapp_router = APIRouter()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN=os.getenv("WHATSAPP_VERIFY_TOKEN")

connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

async def download_media(media_id: str) -> bytes:
    """Download media from WhatsApp."""
    media_metadata_url = f"https://graph.facebook.com/v21.0/{media_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    async with httpx.AsyncClient() as client:
        metadata_response = await client.get(media_metadata_url, headers=headers)
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
        download_url = metadata.get("url")

        media_response = await client.get(download_url, headers=headers)
        media_response.raise_for_status()
        return media_response.content

async def process_audio_message(message):
    """Download and transcribe audio message."""
    audio_id = message["audio"]["id"]
    media_metadata_url = f"https://graph.facebook.com/v21.0/{audio_id}"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    async with httpx.AsyncClient() as client:
        metadata_response = await client.get(media_metadata_url, headers=headers)
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
        download_url = metadata.get("url")

    async with httpx.AsyncClient() as client:
        audio_response = await client.get(download_url, headers=headers)
        audio_response.raise_for_status()
    audio_buffer = BytesIO(audio_response.content)
    audio_buffer.seek(0)
    audio_data = audio_buffer.read()
    return await speech_to_text.transcribe(audio_data)



async def upload_media(media_content: BytesIO, mime_type: str) -> str:
    """Upload media to WhatsApp servers."""
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    files = {"file": ("response.mp3", media_content, mime_type)}
    data = {"messaging_product": "whatsapp", "type": mime_type}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/media",
            headers=headers,
            files=files,
            data=data,
        )
        result = response.json()

    if "id" not in result:
        raise Exception("Failed to upload media")
    return result["id"]

async def send_response(
    from_number: str,
    response_text: str,
    message_type: str = "text",
    media_content: bytes = None,
) -> bool:
    """Send response to user via WhatsApp API."""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }

    if message_type in ["audio", "image"]:
        try:
            mime_type = "audio/mpeg" if message_type == "audio" else "image/png"
            media_buffer = BytesIO(media_content)
            media_id = await upload_media(media_buffer, mime_type)
            json_data = {
                "messaging_product": "whatsapp",
                "to": from_number,
                "type": message_type,
                message_type: {"id": media_id},
            }

            # Add caption for images
            if message_type == "image":
                json_data["image"]["caption"] = response_text
        except Exception as e:
            logger.error(f"Media upload failed, falling back to text: {e}")
            message_type = "text"

    if message_type == "text":
        json_data = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": response_text},
        }

    print(headers)
    print(json_data)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages",
            headers=headers,
            json=json_data,
        )

    return response.status_code == 200



@whatsapp_router.api_route("/whatsapp_response", methods=["GET", "POST"])
async def whatsapp_handler(request: Request) -> Response:
    """Handles incoming messages and status updates from the WhatsApp Cloud API."""

    if request.method == "GET":
        params = request.query_params
        if params.get("hub.verify_token") == WHATSAPP_VERIFY_TOKEN:
            logger.info("Webhook verified successfully.")
            return Response(content=params.get("hub.challenge"), status_code=200)
        logger.warning("Verification token mismatch.")
        return Response(content="Verification token mismatch", status_code=403)

    try:
        data = await request.json()
        logger.info(f"Received data: {data}")

        change_value = data["entry"][0]["changes"][0]["value"]

        if "messages" in change_value:
            message = change_value["messages"][0]
            from_number = message["from"]
            session_id = from_number
            logger.info(f"Incoming message from {from_number}")
            content = ""

            if message["type"] == "audio":
                logger.info("Processing audio message")
                content = await process_audio_message(message)

            elif message["type"] == "image":
                logger.info("Processing image message")
                content = message.get("image", {}).get("caption", "")
                image_bytes = await download_media(message["image"]["id"])
                try:
                    description = await analyze_image(
                        image_bytes,
                        "Please describe what you see in this image in the context of our conversation.",
                    )
                    content += f"\n[Image Analysis: {description}]"
                except Exception as e:
                    logger.warning(f"Failed to analyze image: {e}")

            else:
                logger.info("Processing text message")
                content = message["text"]["body"]

            try:
                logger.info("Running graph with DB checkpointing...")
                async with AsyncConnectionPool(
                    conninfo=os.getenv('SHORT_TERM_MEMORY_DB_PATH'),
                    max_size=20,
                    kwargs=connection_kwargs,
                ) as pool:
                    checkpointer = AsyncPostgresSaver(pool)
                    graph = create_workflow_graph().compile(checkpointer=checkpointer)
                    await graph.ainvoke(
                        {"messages": [HumanMessage(content=content)]},
                        {"configurable": {"thread_id": session_id}},
                    )
                    output_state = await graph.aget_state(config={"configurable": {"thread_id": session_id}})
            except Exception as e:
                logger.error(f"Error invoking graph. Retrying with fresh setup. Error: {e}")
                async with AsyncConnectionPool(
                    conninfo=os.getenv('SHORT_TERM_MEMORY_DB_PATH'),
                    max_size=20,
                    kwargs=connection_kwargs,
                ) as pool:
                    checkpointer = AsyncPostgresSaver(pool)
                    await checkpointer.setup()
                    graph = create_workflow_graph().compile(checkpointer=checkpointer)
                    await graph.ainvoke(
                        {"messages": [HumanMessage(content=content)]},
                        {"configurable": {"thread_id": session_id}},
                    )
                    output_state = await graph.aget_state(config={"configurable": {"thread_id": session_id}})

            workflow = output_state.values.get("workflow", "conversation")
            response_message = output_state.values["messages"][-1].content
            logger.info(f"Generated response for {workflow}: {response_message[:80]}...")

            if workflow == "audio":
                audio_buffer = output_state.values["audio_buffer"]
                success = await send_response(from_number, response_message, "audio", audio_buffer)
            elif workflow == "image":
                image_path = output_state.values["image_path"]
                with open(image_path, "rb") as f:
                    image_data = f.read()
                success = await send_response(from_number, response_message, "image", image_data)
                if os.path.exists(image_path):
                    os.remove(image_path)
            else:
                success = await send_response(from_number, response_message, "text")

            if not success:
                logger.error("Failed to send WhatsApp response.")
                return Response(content="Failed to send message", status_code=500)

            return Response(content="Message processed", status_code=200)

        elif "statuses" in change_value:
            logger.info("Status update received.")
            return Response(content="Status update received", status_code=200)

        else:
            logger.warning("Unknown event type received.")
            return Response(content="Unknown event type", status_code=400)

    except Exception as e:
        logger.exception("Unhandled exception occurred in /whatsapp_response endpoint.")
        return Response(content="Internal server error", status_code=500)
