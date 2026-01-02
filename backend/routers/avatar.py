"""
Avatar Router - Cloud avatar synthesis using D-ID API
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

from core.utils import generate_avatar_video, get_avatar_status
from schemas.avatar import AvatarRequest, AvatarResponse

router = APIRouter()


@router.post("/generate", response_model=AvatarResponse)
async def generate_avatar(request: AvatarRequest):
    """
    Generate talking avatar video using D-ID API

    Args:
        request: Avatar configuration (text, voice, presenter)

    Returns:
        Video URL and generation status
    """
    try:
        result = await generate_avatar_video(
            text=request.text,
            voice_id=request.voice_id,
            presenter_id=request.presenter_id
        )

        return AvatarResponse(
            video_url=result["video_url"],
            duration=result.get("duration"),
            status=result["status"],
            job_id=result.get("job_id")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar generation failed: {str(e)}")


@router.get("/status/{job_id}", response_model=AvatarResponse)
async def check_avatar_status(job_id: str):
    """
    Check status of avatar video generation
    D-ID API processes videos asynchronously

    Args:
        job_id: D-ID job identifier

    Returns:
        Generation status and video URL when ready
    """
    try:
        result = await get_avatar_status(job_id)

        return AvatarResponse(
            video_url=result.get("video_url"),
            duration=result.get("duration"),
            status=result["status"],
            job_id=result["job_id"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check avatar status: {str(e)}")


@router.get("/voices")
async def list_available_voices():
    """
    Get list of available voice options from D-ID

    Returns:
        List of voice IDs and metadata
    """
    # TODO: Fetch from D-ID API
    return {
        "voices": [
            {"id": "en-US-JennyNeural", "name": "Jenny (US English)", "gender": "female"},
            {"id": "en-US-GuyNeural", "name": "Guy (US English)", "gender": "male"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia (UK English)", "gender": "female"},
        ]
    }


@router.get("/presenters")
async def list_available_presenters():
    """
    Get list of available avatar presenters

    Returns:
        List of presenter IDs and preview images
    """
    return {
        "presenters": [
            {"id": "amy", "name": "Amy", "preview": "/static/avatars/amy.jpg"},
            {"id": "david", "name": "David", "preview": "/static/avatars/david.jpg"},
        ]
    }
