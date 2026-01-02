"""
Avatar Schemas - Pydantic models for avatar generation
"""

from pydantic import BaseModel, Field
from typing import Optional


class AvatarRequest(BaseModel):
    """Request model for avatar video generation"""
    text: str = Field(..., description="Text to be spoken")
    voice_id: str = Field("en-US-JennyNeural", description="Voice selection")
    presenter_id: str = Field("amy", description="Avatar presenter")


class AvatarResponse(BaseModel):
    """Response model for avatar generation"""
    video_url: Optional[str] = Field(None, description="Generated video URL")
    duration: Optional[float] = Field(None, description="Video duration in seconds")
    status: str = Field(..., description="Generation status")
    job_id: Optional[str] = Field(None, description="D-ID job ID")


class VoiceOption(BaseModel):
    """Available voice option"""
    id: str
    name: str
    gender: str
    language: Optional[str] = None


class PresenterOption(BaseModel):
    """Available avatar presenter"""
    id: str
    name: str
    preview: str  # URL to preview image
