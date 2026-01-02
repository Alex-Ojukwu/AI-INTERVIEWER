"""
Video Stream Service - WebSocket video frame handler
"""

import cv2
import base64
import numpy as np
from typing import Optional, Callable
import asyncio


class VideoStreamHandler:
    """
    Handles real-time video streaming via WebSocket
    Processes frames for emotion detection
    """

    def __init__(self):
        self.is_streaming = False
        self.frame_callback: Optional[Callable] = None

    def decode_frame(self, base64_image: str) -> Optional[np.ndarray]:
        """
        Decode base64 encoded frame to OpenCV format

        Args:
            base64_image: Base64 encoded image string

        Returns:
            OpenCV image array or None
        """
        try:
            # Remove data URL prefix if present
            if "base64," in base64_image:
                base64_image = base64_image.split("base64,")[1]

            # Decode base64
            image_data = base64.b64decode(base64_image)

            # Convert to numpy array
            nparr = np.frombuffer(image_data, np.uint8)

            # Decode image
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            return frame

        except Exception as e:
            print(f"Error decoding frame: {str(e)}")
            return None

    def encode_frame(self, frame: np.ndarray) -> str:
        """
        Encode OpenCV frame to base64

        Args:
            frame: OpenCV image array

        Returns:
            Base64 encoded string
        """
        try:
            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)

            # Convert to base64
            base64_image = base64.b64encode(buffer).decode('utf-8')

            return f"data:image/jpeg;base64,{base64_image}"

        except Exception as e:
            print(f"Error encoding frame: {str(e)}")
            return ""

    async def process_frame_stream(
        self,
        websocket,
        frame_processor: Callable
    ):
        """
        Process incoming video frames from WebSocket

        Args:
            websocket: WebSocket connection
            frame_processor: Function to process each frame
        """
        self.is_streaming = True

        try:
            while self.is_streaming:
                # Receive frame data
                data = await websocket.receive_json()

                if data.get("type") == "video_frame":
                    # Decode frame
                    frame = self.decode_frame(data["image"])

                    if frame is not None:
                        # Process frame
                        result = await frame_processor(frame)

                        # Send result back
                        await websocket.send_json({
                            "type": "analysis_result",
                            "data": result
                        })

                elif data.get("type") == "stop_stream":
                    self.is_streaming = False
                    break

        except Exception as e:
            print(f"Stream processing error: {str(e)}")
            self.is_streaming = False

    def stop_streaming(self):
        """Stop video stream processing"""
        self.is_streaming = False

    @staticmethod
    def resize_frame(
        frame: np.ndarray,
        max_width: int = 640
    ) -> np.ndarray:
        """
        Resize frame for faster processing

        Args:
            frame: Input frame
            max_width: Maximum width

        Returns:
            Resized frame
        """
        height, width = frame.shape[:2]

        if width > max_width:
            ratio = max_width / width
            new_height = int(height * ratio)
            frame = cv2.resize(frame, (max_width, new_height))

        return frame

    @staticmethod
    def add_overlay(
        frame: np.ndarray,
        text: str,
        position: tuple = (10, 30),
        color: tuple = (0, 255, 0)
    ) -> np.ndarray:
        """
        Add text overlay to frame

        Args:
            frame: Input frame
            text: Text to display
            position: (x, y) position
            color: BGR color tuple

        Returns:
            Frame with overlay
        """
        cv2.putText(
            frame,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            cv2.LINE_AA
        )
        return frame
