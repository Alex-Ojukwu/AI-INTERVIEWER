"""
Interview Router - Main interview orchestration endpoints
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import List, Dict
import json
import asyncio

from core.interview_flow import InterviewFlow
from schemas.interview import InterviewStart, InterviewResponse, QuestionRequest

router = APIRouter()

# Active interview sessions
active_sessions: Dict[str, InterviewFlow] = {}


@router.post("/start", response_model=InterviewResponse)
async def start_interview(request: InterviewStart):
    """
    Start a new interview session

    Args:
        request: Interview configuration (job role, difficulty, etc.)

    Returns:
        InterviewResponse with session_id and first question
    """
    try:
        # Create new interview flow instance
        interview = InterviewFlow(
            job_role=request.job_role,
            difficulty=request.difficulty,
            duration_minutes=request.duration_minutes
        )

        # Generate session ID
        session_id = interview.session_id
        active_sessions[session_id] = interview

        # Get first question
        first_question = await interview.get_next_question()

        return InterviewResponse(
            session_id=session_id,
            question=first_question,
            question_number=1,
            total_questions=interview.total_questions,
            status="active"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@router.post("/answer/{session_id}")
async def submit_answer(session_id: str, request: QuestionRequest):
    """
    Submit an answer and get the next question

    Args:
        session_id: Active interview session ID
        request: User's answer text

    Returns:
        Next question or interview completion status
    """
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")

    interview = active_sessions[session_id]

    try:
        # Process the answer
        await interview.process_answer(request.answer_text)

        # Check if interview is complete
        if interview.is_complete():
            return InterviewResponse(
                session_id=session_id,
                question=None,
                question_number=interview.current_question_number,
                total_questions=interview.total_questions,
                status="completed",
                summary=await interview.generate_summary()
            )

        # Get next question
        next_question = await interview.get_next_question()

        return InterviewResponse(
            session_id=session_id,
            question=next_question,
            question_number=interview.current_question_number,
            total_questions=interview.total_questions,
            status="active"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing answer: {str(e)}")


@router.get("/status/{session_id}")
async def get_interview_status(session_id: str):
    """Get current interview session status"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Interview session not found")

    interview = active_sessions[session_id]

    return {
        "session_id": session_id,
        "current_question": interview.current_question_number,
        "total_questions": interview.total_questions,
        "elapsed_time": interview.get_elapsed_time(),
        "status": "completed" if interview.is_complete() else "active"
    }


@router.delete("/end/{session_id}")
async def end_interview(session_id: str):
    """End and cleanup an interview session"""
    if session_id in active_sessions:
        interview = active_sessions[session_id]
        summary = await interview.generate_summary()
        del active_sessions[session_id]

        return {
            "message": "Interview ended successfully",
            "summary": summary
        }

    raise HTTPException(status_code=404, detail="Interview session not found")


@router.websocket("/ws/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    """
    WebSocket connection for real-time interview interaction
    Handles video frames, audio, and emotion data
    """
    await websocket.accept()

    if session_id not in active_sessions:
        await websocket.close(code=4004, reason="Invalid session")
        return

    try:
        while True:
            # Receive data from client
            data = await websocket.receive_json()

            # Handle different message types
            if data["type"] == "emotion_data":
                # Store emotion data
                pass

            elif data["type"] == "audio_chunk":
                # Process audio chunk
                pass

            # Send acknowledgment
            await websocket.send_json({"status": "received"})

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for session: {session_id}")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.close(code=1011, reason=str(e))
