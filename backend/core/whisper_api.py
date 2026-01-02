"""
Whisper API Module - OpenAI Whisper for speech-to-text transcription
"""

from openai import AsyncOpenAI
from pathlib import Path
from typing import Dict, Optional

from config import settings


class WhisperTranscriber:
    """
    Handles audio transcription using OpenAI Whisper API
    Provides high-accuracy speech-to-text for interview responses
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.WHISPER_MODEL

    async def transcribe(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Transcribe audio file to text

        Args:
            audio_path: Path to audio file
            language: Optional language code (e.g., 'en')
            prompt: Optional context prompt for better accuracy

        Returns:
            Transcription result with text and metadata
        """
        try:
            with open(audio_path, "rb") as audio_file:
                # Call Whisper API
                response = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language,
                    prompt=prompt,
                    response_format="verbose_json"
                )

            # Extract response data
            result = {
                "text": response.text,
                "language": response.language if hasattr(response, 'language') else None,
                "duration": response.duration if hasattr(response, 'duration') else None,
                "segments": response.segments if hasattr(response, 'segments') else None
            }

            # Calculate confidence (if segments available)
            if result["segments"]:
                avg_confidence = sum(
                    seg.get("avg_logprob", 0) for seg in result["segments"]
                ) / len(result["segments"])
                result["confidence"] = avg_confidence
            else:
                result["confidence"] = None

            return result

        except Exception as e:
            print(f"Transcription error: {str(e)}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")

    async def transcribe_with_timestamps(
        self,
        audio_path: Path
    ) -> Dict[str, any]:
        """
        Transcribe with word-level timestamps

        Args:
            audio_path: Path to audio file

        Returns:
            Transcription with word timestamps
        """
        try:
            with open(audio_path, "rb") as audio_file:
                response = await self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )

            return {
                "text": response.text,
                "words": response.words if hasattr(response, 'words') else None,
                "duration": response.duration if hasattr(response, 'duration') else None
            }

        except Exception as e:
            print(f"Timestamp transcription error: {str(e)}")
            raise Exception(f"Failed to transcribe with timestamps: {str(e)}")

    async def translate_to_english(
        self,
        audio_path: Path
    ) -> Dict[str, str]:
        """
        Translate non-English audio to English

        Args:
            audio_path: Path to audio file

        Returns:
            English translation
        """
        try:
            with open(audio_path, "rb") as audio_file:
                response = await self.client.audio.translations.create(
                    model=self.model,
                    file=audio_file
                )

            return {
                "text": response.text,
                "original_language": "auto-detected"
            }

        except Exception as e:
            print(f"Translation error: {str(e)}")
            raise Exception(f"Failed to translate audio: {str(e)}")
