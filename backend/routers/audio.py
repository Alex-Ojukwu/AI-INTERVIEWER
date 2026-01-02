"""
Audio Router - Handles audio upload and Whisper API transcription
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
import os

from core.whisper_api import WhisperTranscriber
from config import settings

router = APIRouter()
transcriber = WhisperTranscriber()


@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """
    Transcribe audio file using Whisper API

    Args:
        audio: Audio file (mp3, wav, m4a, webm)

    Returns:
        Transcription text and metadata
    """
    # Validate file type
    allowed_extensions = {".mp3", ".wav", ".m4a", ".webm", ".ogg"}
    file_ext = Path(audio.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Check file size
    content = await audio.read()
    file_size_mb = len(content) / (1024 * 1024)

    if file_size_mb > settings.MAX_AUDIO_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_AUDIO_SIZE_MB}MB"
        )

    # Save temporary file
    temp_filename = f"{uuid.uuid4()}{file_ext}"
    temp_path = settings.TEMP_AUDIO_DIR / temp_filename

    try:
        # Write audio to temp file
        with open(temp_path, "wb") as f:
            f.write(content)

        # Transcribe using Whisper API
        result = await transcriber.transcribe(temp_path)

        return {
            "success": True,
            "transcription": result["text"],
            "language": result.get("language"),
            "duration": result.get("duration"),
            "confidence": result.get("confidence")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    finally:
        # Cleanup temp file
        if temp_path.exists():
            os.remove(temp_path)


@router.post("/stream-transcribe")
async def stream_transcribe(audio: UploadFile = File(...)):
    """
    Stream audio transcription for real-time processing
    Useful for live interview responses
    """
    # TODO: Implement streaming transcription
    pass
