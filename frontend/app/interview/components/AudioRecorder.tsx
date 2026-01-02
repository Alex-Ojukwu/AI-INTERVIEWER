"use client";

import { useState, useRef } from "react";
import { transcribeAudio } from "@/lib/api";
import { startRecording, stopRecording } from "@/lib/recorder";

interface AudioRecorderProps {
  onTranscriptionComplete: (text: string) => void;
  disabled?: boolean;
}

export default function AudioRecorder({
  onTranscriptionComplete,
  disabled = false,
}: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const handleStartRecording = async () => {
    try {
      const mediaRecorder = await startRecording();
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = handleRecordingStop;

      setIsRecording(true);
    } catch (error) {
      console.error("Failed to start recording:", error);
      alert("Unable to access microphone. Please check permissions.");
    }
  };

  const handleStopRecording = () => {
    if (mediaRecorderRef.current) {
      stopRecording(mediaRecorderRef.current);
      setIsRecording(false);
    }
  };

  const handleRecordingStop = async () => {
    setIsProcessing(true);

    try {
      // Create audio blob
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });

      // Create form data
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      // Transcribe audio
      const result = await transcribeAudio(formData);

      if (result.success) {
        onTranscriptionComplete(result.transcription);
      } else {
        alert("Transcription failed. Please try again.");
      }
    } catch (error) {
      console.error("Transcription error:", error);
      alert("Failed to process audio. Please try again.");
    } finally {
      setIsProcessing(false);
      audioChunksRef.current = [];
    }
  };

  return (
    <div className="audio-recorder">
      {!isRecording && !isProcessing && (
        <button
          onClick={handleStartRecording}
          disabled={disabled}
          className="record-button"
        >
          <span className="mic-icon">🎤</span>
          Start Recording
        </button>
      )}

      {isRecording && (
        <button onClick={handleStopRecording} className="stop-button">
          <span className="recording-dot"></span>
          Stop Recording
        </button>
      )}

      {isProcessing && (
        <div className="processing">
          <span className="spinner"></span>
          Processing audio...
        </div>
      )}
    </div>
  );
}
