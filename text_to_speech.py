import os
from typing_extensions import Optional

from elevenlabs import ElevenLabs, Voice, VoiceSettings
from dotenv import load_dotenv

load_dotenv()


class TextToSpeech:
    def __init__(self):
        self._client: Optional[ElevenLabs] = None

    @property
    def client(self) -> ElevenLabs:
        """Get or create ElevenLabs client instance using singleton pattern."""
        if self._client is None:
            self._client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        return self._client

    async def synthesize(self, text: str):
        if not text.strip():
            raise ValueError("Input text cannot be empty")
        if len(text) > 5000:  # ElevenLabs typical limit
            raise ValueError("Input text exceeds maximum length of 5000 characters")

        try:
            audio_generator = self.client.generate(
                text=text,
                voice=Voice(
                    voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
                    settings=VoiceSettings(stability=0.5, similarity_boost=0.5),
                ),
                model="eleven_flash_v2_5",
            )
            audio_bytes = b"".join(audio_generator)
            return audio_bytes
        except Exception as e:
            raise ValueError(e)
