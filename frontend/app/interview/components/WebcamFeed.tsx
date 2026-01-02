"use client";

import { useEffect, useRef, useState } from "react";
import { analyzeEmotion } from "@/lib/api";

interface WebcamFeedProps {
  onEmotionUpdate?: (emotionData: any) => void;
}

export default function WebcamFeed({ onEmotionUpdate }: WebcamFeedProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    startWebcam();
    return () => {
      stopWebcam();
    };
  }, []);

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
        audio: false,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsStreaming(true);
        setError(null);

        // Start emotion analysis interval (every 2 seconds)
        intervalRef.current = setInterval(() => {
          captureAndAnalyze();
        }, 2000);
      }
    } catch (err) {
      console.error("Error accessing webcam:", err);
      setError("Unable to access webcam. Please check permissions.");
    }
  };

  const stopWebcam = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach((track) => track.stop());
      setIsStreaming(false);
    }

    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
  };

  const captureAndAnalyze = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;

    // Draw video frame to canvas
    const context = canvas.getContext("2d");
    if (context) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      context.drawImage(video, 0, 0);

      // Convert to base64
      const imageData = canvas.toDataURL("image/jpeg", 0.8);

      try {
        // Send to emotion analysis API
        const result = await analyzeEmotion(imageData);

        if (onEmotionUpdate) {
          onEmotionUpdate(result);
        }
      } catch (error) {
        console.error("Emotion analysis failed:", error);
      }
    }
  };

  return (
    <div className="webcam-feed">
      {error && <div className="error-message">{error}</div>}

      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="webcam-video"
      />

      <canvas ref={canvasRef} style={{ display: "none" }} />

      {isStreaming && (
        <div className="streaming-indicator">
          <span className="indicator-dot"></span> Live
        </div>
      )}
    </div>
  );
}
