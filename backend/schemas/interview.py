"""
Interview Schemas - Pydantic models for interview endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class InterviewStart(BaseModel):
    """Request model for starting an interview"""
    job_role: str = Field(..., description="Target job position")
    difficulty: str = Field("medium", description="Interview difficulty level")
    duration_minutes: int = Field(30, ge=5, le=60, description="Interview duration")
    candidate_name: Optional[str] = Field(None, description="Candidate name")


class InterviewResponse(BaseModel):
    """Response model for interview questions"""
    session_id: str
    question: Optional[str] = None
    question_number: int
    total_questions: int
    status: str  # "active" or "completed"
    summary: Optional[Dict] = None


class QuestionRequest(BaseModel):
    """Request model for submitting an answer"""
    answer_text: str = Field(..., description="Candidate's answer")
    audio_url: Optional[str] = Field(None, description="Audio recording URL")


class InterviewSummary(BaseModel):
    """Complete interview summary"""
    session_id: str
    job_role: str
    duration_minutes: float
    questions_asked: int
    qa_pairs: List[Dict]
    emotion_analysis: Dict
    ai_assessment: Dict
    completed_at: str
