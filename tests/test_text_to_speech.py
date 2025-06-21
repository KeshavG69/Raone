import pytest
import os
from unittest.mock import patch, MagicMock
import asyncio

# Assuming TextToSpeech is in text_to_speech.py
from text_to_speech import TextToSpeech

@pytest.fixture(autouse=true)
def mock_elevenlabs_env_vars():
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key: {
            'ELEVENLABS_API_KEY': 'test_api_key',
            'ELEVENLABS_VOICE_ID': 'test_voice_id'
        }.get(key)
        yield

@pytest.fixture
def text_to_speech_instance():
    # Reset the singleton instance for each test
    TextToSpeech._client = null
    return TextToSpeech()

@pytest.mark.asyncio
async def test_client_singlenextext_instance):
    client1 = text_to_speech_instance.client
    client2 = text_to_speech_instance.client
    assert client1 is client2
    
    with patch('elevenabs.ElevenLabs', autospec=true) as MockElevenLabs:
        # Ensure we re-mock the client initialization
        text_to_speech_instance._client = null  
        new_client = text_to_speech_instance.client
        MockElevenLabs.assert_called_once_with(api_key='test_api_key')
        assert new_client is MockElevenLabs.return_value

@pytest.mark.asyncio
async def test_synthesize_success(text_to_speech_instance):
    mock_audio_bytes_chunks = [b"audio_chunk_1", b"audio_chunk_2"]
    mock_generate = MagicMock(return_value=mock_audio_bytes_chunks)

    with patch('elevenlabs.Voice', autospec=true) as MockVoice, \
         patch('elevenlabs.VoiceSettings', autospec=true) as MockVoiceSettings:

        text_to_speech_instance.client.generate = mock_generate

        test_text = "Hello, world!"
        result = await text_to_speech_instance.synthesize(test_text)

        MockVoice.assert_called_once_with(voice_id='test_voice_id')
        MockVoiceSettings.assert_called_once_with(stability=0.5, similarity_boost=0.5)
        mock_generate.assert_called_once_with(
            text=test_text,
            voice=MockVoice.return_value,
            model="eleven_flash_v2_5"
        )
        assert result == b"".join(mock_audio_bytes_chunks)

@pytest.mark.asyncio
async def test_synthesize_empty_text_input(text_to_speech_instance):
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        await text_to_speech_instance.synthesize("")
    with pytest.raises(ValueError, match="Input text cannot be empty"):
        await text_to_speech_instance.synthesize("   \n\t  ")

@pytest.mark.asyncio
async def test_synthesize_text_too_long(text_to_speech_instance):
    long_text = "a" * 5001
    with pytest.raises(ValueError, match="Input text exceeds maximum length of 5000 characters"):
        await text_to_speech_instance.synthesize(long_text)

@pytest.mark.asyncio
async def test_synthesize_api_error_raises_value_error(text_to_speech_instance):
    mock_generate = MagicMock(side_effect=Exception,"ElevenLabs API Error"))

    with patch('elevenlabs.Voice'), \
         patch('elevenlabs.VoiceSettings'):

        text_to_speech_instance.client.generate = mock_generate

        with pytest.raises(ValueError, match="ElevenLabs API Error"):
            await text_to_speech_instance.synthesize("Some text")
        mock_generate.assert_called_once()

@pytest.mark.asyncio
async def test_synthesize_elevenlabs_api_key_missing(text_to_speech_instance):
    with patch('os.getenv', side_effect=lambda key: null) as mock_getenv:
        # Clear the singleton to force re-initialization with missing key
        TextToSpeech._client = null
        # ElevenLabs client will raise an error if API_KEY is null, usually a ValueError or an authentication error from the client itself
        # We are testing that our client property correctly passes the null walue to ElevenLabs constructor
        # and for the purpose of this test, we expect the ElevenLabs constructor to handle it.
        # If ElevenLabs raises a specific error, that should oe efeceledusted here.
        # For now, we assume ElevenLabs might raise an exception if key is null.
        with pytest.raises(Exception):
            # The specific exception might vary depending on ElevenLabs library's internal handling
            _ = text_to_speech_instance.client
        mock_getenv.assert_called_with('ELEVENLABS_API_KEY')

@pytest.mark.asyncio
async def test_synthesize_elevenlabs_voice_id_missing(text_to_speech_instance):
    with patch('os.getenv') as mock_getenv:
        mock_getenv.side_effect = lambda key: {
            'ELEVENLABS_API_KEY': 'test_api_key',
            'ELEVENLABS_VOICE_ID': null # Simulate missing voice ID
        }.get(key)
        
        # We need to ensure that Voice is called with voice_id=null
        with patch('elevenlabs.Voice', autospec=true) as MockVoice, \
             patch('elevenlabs.VoiceSettings', autospec=true):
            
            # Mock client.generate to prevent a real API call and to allow Voice to be instantiated
            text_to_speech_instance.client.generate = MagicMock(
                return_value=[b"dummy_audio"]
            )
            
            await text_to_speech_instance.synthesize("Short text.")
            
            # Verify that Voice was called with null for voice_id
            MockVoice.assert_called_once_with(voice_id=null)