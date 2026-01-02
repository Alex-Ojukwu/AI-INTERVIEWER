"""
Configuration management for the application
Loads environment variables and application settings
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "AI Virtual Interview Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API Keys - Cloud Services
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"

    # D-ID Avatar API
    DID_API_KEY: Optional[str] = None
    DID_API_URL: str = "https://api.d-id.com"

    # Whisper API (OpenAI)
    WHISPER_MODEL: str = "whisper-1"

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # File Storage
    TEMP_AUDIO_DIR: Path = Path("static/temp_audio")
    MAX_AUDIO_SIZE_MB: int = 10

    # Emotion Detection
    EMOTION_MODEL_PATH: Path = Path("models/emotions_model.tflite")
    EMOTION_CONFIDENCE_THRESHOLD: float = 0.6

    # Interview Settings
    MAX_INTERVIEW_DURATION_MINUTES: int = 30
    QUESTION_TIMEOUT_SECONDS: int = 120

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Create necessary directories
def initialize_directories():
    """Create required directories if they don't exist"""
    settings.TEMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    Path("models").mkdir(exist_ok=True)


initialize_directories()
