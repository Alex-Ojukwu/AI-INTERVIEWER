"""
Emotion Router - Handles facial expression analysis requests
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Dict, List
import base64
import numpy as np
import cv2
import sys
import logging

from services.face_analysis import FaceAnalyzer
from schemas.emotion import EmotionResponse, EmotionFrame

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()
face_analyzer = FaceAnalyzer()


@router.post("/analyze", response_model=EmotionResponse)
async def analyze_emotion(image: UploadFile = File(...)):
    """
    Analyze facial emotions from uploaded image

    Args:
        image: Image file containing a face

    Returns:
        Detected emotions with confidence scores
    """
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        # Analyze emotions
        result = face_analyzer.analyze_frame(img)

        return EmotionResponse(
            emotions=result["emotions"],
            dominant_emotion=result["dominant_emotion"],
            confidence=result["confidence"],
            face_detected=result["face_detected"],
            face_landmarks=result.get("landmarks")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotion analysis failed: {str(e)}")


@router.post("/analyze-base64")
async def analyze_emotion_base64(data: Dict[str, str]):
    """
    Analyze emotions from base64 encoded image
    Useful for WebSocket/real-time streaming

    Args:
        data: {"image": "base64_string"}

    Returns:
        Emotion analysis results
    """
    try:
        logger.info("Decoding base64 image...")
        print("[1] Decoding base64 image...", flush=True)

        # Decode base64 image
        image_data = base64.b64decode(data["image"])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            logger.error("Failed to decode image - img is None")
            print("[ERROR] Failed to decode image", flush=True)
            raise HTTPException(status_code=400, detail="Invalid image data")

        logger.info(f"Image decoded: shape={img.shape}")
        print(f"[2] Image decoded: shape={img.shape}", flush=True)

        # Analyze emotions with DeepFace
        logger.info("Calling DeepFace analyze_frame...")
        print("[3] Calling face_analyzer.analyze_frame()...", flush=True)

        result = face_analyzer.analyze_frame(img)

        logger.info(f"Analysis complete: {result}")
        print(f"[4] Analysis result: {result}", flush=True)

        return result

    except KeyError as e:
        error_msg = f"KeyError: {e}"
        logger.error(error_msg)
        print(f"[ERROR] {error_msg}", flush=True)
        raise HTTPException(status_code=400, detail="Missing 'image' field in request")
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Exception in analyze_emotion_base64: {error_msg}")
        print(f"[ERROR] Exception: {error_msg}", flush=True)

        import traceback
        tb = traceback.format_exc()
        logger.error(tb)
        print(f"[ERROR] Traceback:\n{tb}", flush=True)

        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/batch-analyze")
async def batch_analyze_emotions(frames: List[EmotionFrame]):
    """
    Analyze multiple frames for emotion tracking over time

    Args:
        frames: List of base64 encoded frames with timestamps

    Returns:
        Aggregated emotion analysis
    """
    results = []

    for frame in frames:
        try:
            # Decode image
            image_data = base64.b64decode(frame.image_data)
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Analyze
            result = face_analyzer.analyze_frame(img)
            result["timestamp"] = frame.timestamp
            results.append(result)

        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            continue

    # Compute aggregated metrics
    if results:
        aggregated = face_analyzer.aggregate_emotions(results)
        return {
            "frames_analyzed": len(results),
            "aggregated_emotions": aggregated,
            "timeline": results
        }

    return {"error": "No frames could be analyzed"}


@router.get("/health")
async def emotion_service_health():
    """Check if emotion detection service is ready"""
    return {
        "status": "healthy",
        "model_loaded": face_analyzer.is_model_loaded(),
        "backend": "DeepFace + TensorFlow"
    }


@router.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify routing works"""
    logger.info("TEST ENDPOINT CALLED!")
    sys.stdout.flush()
    return {"status": "ok", "message": "Routing works!"}
