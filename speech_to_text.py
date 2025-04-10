from groq import Groq
from typing_extensions import Optional
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()  # take environment variables

class SpeechToText():
    def __init__(self):
        self._client: Optional[Groq] = None

    @property
    def client(self) -> Groq:
        """Get or create Groq client instance using singleton pattern."""
        if self._client is None:
            self._client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        return self._client


    async def transcribe(self, audio_data: bytes) -> Optional[str]:
        if not audio_data:
            raise ValueError("Audio data cannot be empty")

        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name

            try:
                with open(temp_file_path, "rb") as audio_file:
                    transcription =  self.client.audio.transcriptions.create(
                        file=audio_file,
                        model="whisper-large-v3-turbo",
                        language="en",
                        response_format="text",
                    )
                return transcription
            finally:
                try:
                    os.unlink(temp_file_path)
                except OSError as e:
                    print(f"Warning: Could not delete temp file: {e}")

        except Exception as e:
            print(f"Error during transcription: {e}")
            return None