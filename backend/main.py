"""
AI Virtual Interview Assistant - FastAPI Backend
Main entry point for the FastAPI application
"""

# Fix Unicode encoding issues on Windows
import sys
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == 'win32':
    # Force UTF-8 encoding for stdout/stderr
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from routers import interview, audio, emotion, avatar

app = FastAPI(
    title="AI Virtual Interview Assistant",
    description="Backend API for AI-powered virtual interviews with emotion detection",
    version="1.0.0"
)

# CORS configuration for Next.js frontend
from config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS] if isinstance(settings.CORS_ORIGINS, str) else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(interview.router, prefix="/api/interview", tags=["Interview"])
app.include_router(audio.router, prefix="/api/audio", tags=["Audio"])
app.include_router(emotion.router, prefix="/api/emotion", tags=["Emotion"])
app.include_router(avatar.router, prefix="/api/avatar", tags=["Avatar"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "AI Virtual Interview Assistant API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "websocket": "ready",
            "emotion_detection": "loaded"
        }
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
