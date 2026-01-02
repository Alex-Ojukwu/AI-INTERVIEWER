"""
Face Analysis Service - DeepFace emotion detection
"""

import cv2
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path
import os
import tempfile

from config import settings


class FaceAnalyzer:
    """
    Analyzes facial expressions and emotions using DeepFace
    Provides accurate emotion detection with pre-trained models
    """

    def __init__(self):
        # Suppress TensorFlow warnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

        # Initialize DeepFace
        try:
            from deepface import DeepFace
            self.DeepFace = DeepFace
            self.deepface_available = True
            print("DeepFace initialized successfully for emotion detection")
        except Exception as e:
            print(f"DeepFace initialization failed: {e}. Using fallback mode.")
            self.DeepFace = None
            self.deepface_available = False

        # Emotion labels (DeepFace uses these)
        self.emotions = [
            "angry", "disgust", "fear", "happy",
            "sad", "surprise", "neutral"
        ]

        # Map DeepFace emotions to our format
        self.emotion_mapping = {
            "angry": "angry",
            "disgust": "disgusted",
            "fear": "fearful",
            "happy": "happy",
            "sad": "sad",
            "surprise": "surprised",
            "neutral": "neutral"
        }

    def analyze_frame(self, frame: np.ndarray) -> Dict[str, any]:
        """
        Analyze single frame for facial emotions using DeepFace

        Args:
            frame: BGR image from webcam

        Returns:
            Emotion analysis results
        """
        if not self.deepface_available:
            # Fallback: return neutral emotion
            return {
                "face_detected": False,
                "emotions": {"neutral": float(1.0)},
                "dominant_emotion": "neutral",
                "confidence": float(0.0)
            }

        try:
            # DeepFace requires image file or numpy array
            # Use enforce_detection=False to handle frames without faces gracefully
            result = self.DeepFace.analyze(
                img_path=frame,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True  # Suppress DeepFace logs
            )

            # Handle result (can be list or dict)
            if isinstance(result, list):
                result = result[0] if len(result) > 0 else None

            if result is None:
                return {
                    "face_detected": False,
                    "emotions": {},
                    "dominant_emotion": None,
                    "confidence": 0.0
                }

            # Extract emotion data
            emotions_raw = result.get('emotion', {})

            # Normalize emotion scores to percentages (0-1 range)
            total = sum(emotions_raw.values())
            if total > 0:
                emotions = {k: float(v / 100.0) for k, v in emotions_raw.items()}
            else:
                emotions = {k: float(v) for k, v in emotions_raw.items()}

            # Map to our emotion format
            mapped_emotions = {}
            for deepface_emotion, our_emotion in self.emotion_mapping.items():
                if deepface_emotion in emotions:
                    mapped_emotions[our_emotion] = float(emotions[deepface_emotion])

            # Get dominant emotion
            dominant_deepface = result.get('dominant_emotion', 'neutral')
            dominant = self.emotion_mapping.get(dominant_deepface, 'neutral')
            confidence = float(mapped_emotions.get(dominant, 0.0))

            # Get face region if available
            face_region = result.get('region', {})

            print(f"[DeepFace] ✓ Face detected! Emotion: {dominant} ({confidence:.1%})")

            return {
                "face_detected": True,
                "emotions": mapped_emotions,
                "dominant_emotion": dominant,
                "confidence": confidence,
                "face_region": face_region
            }

        except Exception as e:
            # Handle errors gracefully (no face detected, etc.)
            print(f"[DeepFace] No face detected or error: {str(e)[:80]}")
            return {
                "face_detected": False,
                "emotions": {},
                "dominant_emotion": None,
                "confidence": float(0.0),
                "error": str(e)
            }


    def aggregate_emotions(
        self,
        emotion_timeline: List[Dict]
    ) -> Dict[str, any]:
        """
        Aggregate multiple emotion readings over time

        Args:
            emotion_timeline: List of emotion analysis results

        Returns:
            Aggregated metrics
        """
        if not emotion_timeline:
            return {}

        # Count dominant emotions
        emotion_counts = {}
        total_confidence = 0

        for data in emotion_timeline:
            if data.get("face_detected"):
                dominant = data.get("dominant_emotion")
                if dominant:
                    emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1
                    total_confidence += data.get("confidence", 0)

        total_frames = len(emotion_timeline)
        avg_confidence = total_confidence / total_frames if total_frames > 0 else 0

        # Calculate percentages
        emotion_percentages = {
            emotion: (count / total_frames) * 100
            for emotion, count in emotion_counts.items()
        }

        return {
            "total_frames": total_frames,
            "emotion_distribution": emotion_percentages,
            "most_common": max(emotion_counts, key=emotion_counts.get) if emotion_counts else None,
            "average_confidence": avg_confidence
        }

    def is_model_loaded(self) -> bool:
        """Check if DeepFace is available"""
        return self.deepface_available

    def __del__(self):
        """Cleanup resources"""
        # DeepFace handles its own cleanup
        pass
