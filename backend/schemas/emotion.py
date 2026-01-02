"""
Emotion Schemas - Pydantic models for emotion analysis
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class EmotionResponse(BaseModel):
    """Response model for emotion analysis"""
    emotions: Dict[str, float] = Field(..., description="Emotion probabilities")
    dominant_emotion: Optional[str] = Field(None, description="Most likely emotion")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")
    face_detected: bool = Field(..., description="Whether a face was detected")
    face_landmarks: Optional[List[Dict]] = Field(None, description="Facial landmarks")


class EmotionFrame(BaseModel):
    """Single frame for batch emotion analysis"""
    image_data: str = Field(..., description="Base64 encoded image")
    timestamp: float = Field(..., description="Frame timestamp")


class EmotionTimeline(BaseModel):
    """Emotion analysis over time"""
    frames_analyzed: int
    aggregated_emotions: Dict[str, float]
    timeline: List[Dict]
    most_common_emotion: Optional[str] = None
