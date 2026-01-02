"""
Utility Functions - Shared helpers for the application
"""

import requests
import json
import base64
from typing import Dict, Optional
from pathlib import Path

from config import settings


async def generate_avatar_video(
    text: str,
    voice_id: str = "en-US-JennyNeural",
    presenter_id: str = "amy"
) -> Dict[str, any]:
    """
    Generate talking avatar video using D-ID API
    D-ID processes videos asynchronously - this initiates the job

    Args:
        text: Text to be spoken
        voice_id: Voice selection
        presenter_id: Avatar presenter ID

    Returns:
        Job information (status will be 'created' or 'pending', video_url available after polling)
    """
    if not settings.DID_API_KEY:
        raise ValueError("D-ID API key not configured")

    url = f"{settings.DID_API_URL}/talks"

    # D-ID uses non-standard Basic Auth format: Basic API_USERNAME:API_PASSWORD
    # The DID_API_KEY should be in format "username:password" (plain text)
    # NOTE: D-ID does NOT require base64 encoding unlike standard Basic auth
    credentials = settings.DID_API_KEY.strip()

    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

    # Use a publicly accessible image URL
    # Using D-ID's sample image from their documentation examples
    payload = {
        "script": {
            "type": "text",
            "input": text,
            "provider": {
                "type": "microsoft",
                "voice_id": voice_id
            }
        },
        # Use D-ID's public sample presenter image
        "source_url": "https://d-id-public-bucket.s3.us-west-2.amazonaws.com/alice.jpg",
        "config": {
            "fluent": True,
            "pad_audio": 0.0
        }
    }

    try:
        # Make request to D-ID
        print(f"[D-ID] Sending request to: {url}")
        print(f"[D-ID] Auth header (masked): Basic {'*' * 20}")
        print(f"[D-ID] Payload: {json.dumps(payload, indent=2)}")

        response = requests.post(url, headers=headers, json=payload)

        print(f"[D-ID] Response status: {response.status_code}")
        print(f"[D-ID] Response body: {response.text[:500]}")

        response.raise_for_status()

        result = response.json()

        # D-ID returns: {id, status, created_at, ...}
        # Status will be "created" or "pending" initially
        # result_url only appears when status becomes "done"
        return {
            "job_id": result.get("id"),
            "status": result.get("status", "pending"),
            "video_url": result.get("result_url"),  # Will be None initially
            "duration": result.get("duration"),
            "created_at": result.get("created_at")
        }

    except requests.exceptions.RequestException as e:
        error_detail = response.text if 'response' in locals() else str(e)
        print(f"[D-ID ERROR] Status: {response.status_code if 'response' in locals() else 'N/A'}")
        print(f"[D-ID ERROR] Details: {error_detail}")
        raise Exception(f"Avatar generation failed: {error_detail}")


async def get_avatar_status(job_id: str) -> Dict[str, any]:
    """
    Check the status of a D-ID avatar generation job

    Args:
        job_id: D-ID job identifier

    Returns:
        Job status information including video_url when ready
    """
    if not settings.DID_API_KEY:
        raise ValueError("D-ID API key not configured")

    url = f"{settings.DID_API_URL}/talks/{job_id}"

    # Same auth as generation - D-ID uses non-standard Basic auth (no base64 encoding)
    credentials = settings.DID_API_KEY.strip()

    headers = {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }

    try:
        print(f"[D-ID] Checking status for job: {job_id}")

        response = requests.get(url, headers=headers)

        print(f"[D-ID] Status response: {response.status_code}")
        print(f"[D-ID] Response body: {response.text[:500]}")

        response.raise_for_status()

        result = response.json()

        # D-ID status can be: "created", "started", "done", "error", "rejected"
        return {
            "job_id": result.get("id"),
            "status": result.get("status"),
            "video_url": result.get("result_url"),  # Available when status is "done"
            "duration": result.get("duration"),
            "created_at": result.get("created_at"),
            "started_at": result.get("started_at"),
            "completed_at": result.get("completed_at"),
            "error": result.get("error")  # Present if status is "error"
        }

    except requests.exceptions.RequestException as e:
        error_detail = response.text if 'response' in locals() else str(e)
        print(f"[D-ID ERROR] Status check failed: {error_detail}")
        raise Exception(f"Failed to get avatar status: {error_detail}")


def validate_audio_file(file_path: Path) -> bool:
    """
    Validate audio file format and size

    Args:
        file_path: Path to audio file

    Returns:
        True if valid, False otherwise
    """
    if not file_path.exists():
        return False

    # Check file extension
    allowed_extensions = {".mp3", ".wav", ".m4a", ".webm", ".ogg"}
    if file_path.suffix.lower() not in allowed_extensions:
        return False

    # Check file size (max 10MB)
    max_size = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024
    if file_path.stat().st_size > max_size:
        return False

    return True


def format_timestamp(seconds: float) -> str:
    """
    Format seconds into MM:SS

    Args:
        seconds: Time in seconds

    Returns:
        Formatted timestamp string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def calculate_engagement_score(emotion_data: Dict) -> float:
    """
    Calculate engagement score from emotion data

    Args:
        emotion_data: Aggregated emotion metrics

    Returns:
        Engagement score (0-100)
    """
    if not emotion_data or "emotion_distribution" not in emotion_data:
        return 50.0  # Neutral default

    distribution = emotion_data["emotion_distribution"]

    # Positive emotions increase score
    positive_emotions = ["happy", "focused", "confident"]
    negative_emotions = ["nervous", "distracted", "confused"]

    positive_score = sum(
        distribution.get(emotion, 0) for emotion in positive_emotions
    )

    negative_score = sum(
        distribution.get(emotion, 0) for emotion in negative_emotions
    )

    # Calculate weighted score
    engagement = 50 + (positive_score / 2) - (negative_score / 2)

    return max(0, min(100, engagement))  # Clamp to 0-100
