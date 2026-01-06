"use client";

import { useEffect, useState, useRef } from "react";
import { generateAvatar } from "@/lib/avatar";

interface AvatarPlayerProps {
  questionText: string;
}

export default function AvatarPlayer({ questionText }: AvatarPlayerProps) {
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isIdle, setIsIdle] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const speechRef = useRef<SpeechSynthesisUtterance | null>(null);
  const lastQuestionRef = useRef<string>("");

  useEffect(() => {
    // Only generate if question changed and not empty
    if (questionText && questionText !== lastQuestionRef.current) {
      lastQuestionRef.current = questionText;
      // Use D-ID avatar generation
      generateAvatarVideo(questionText);
    }
  }, [questionText]);

  const speakWithTTS = (text: string) => {
    // Stop any ongoing speech
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }

    // Wait a moment for cancel to complete
    setTimeout(() => {
      const utterance = new SpeechSynthesisUtterance(text);
      speechRef.current = utterance;

    // Configure voice (use the best quality voice available)
    const voices = window.speechSynthesis.getVoices();

    // Priority order: Premium voices > Neural voices > Standard voices
    const preferredVoice = voices.find(v =>
      v.name.includes('Google') && v.name.includes('en-US') ||
      v.name.includes('Samantha') || // macOS high quality
      v.name.includes('Microsoft Aria') || // Windows 11 neural
      v.name.includes('Microsoft Jenny') || // Windows neural
      v.name.includes('Karen') || // macOS
      v.name.includes('Female')
    ) || voices.find(v => v.lang.startsWith('en-US')) || voices[0];

    if (preferredVoice) {
      utterance.voice = preferredVoice;
      console.log('Using voice:', preferredVoice.name);
    }

    utterance.rate = 0.95; // Natural speaking pace
    utterance.pitch = 1.0; // Natural pitch
    utterance.volume = 1.0;

    utterance.onstart = () => {
      setIsSpeaking(true);
      setIsIdle(false);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      setIsIdle(true);
    };

    utterance.onerror = () => {
      setIsSpeaking(false);
      setIsIdle(true);
    };

      window.speechSynthesis.speak(utterance);
    }, 100); // Small delay to prevent overlap
  };

  const generateAvatarVideo = async (text: string) => {
    setIsLoading(true);
    setError(null);
    setIsIdle(false);

    try {
      const result = await generateAvatar(text);

      if (result.video_url) {
        setVideoUrl(result.video_url);
        setIsIdle(false);
      } else if (result.job_id) {
        setError("Generating avatar video... (15-30 seconds)");
        setTimeout(() => checkAvatarStatus(result.job_id), 2000);
      }
    } catch (err) {
      console.error("Avatar generation failed, using TTS fallback:", err);
      // Use text-to-speech as fallback
      setError(null);
      setIsLoading(false);
      speakWithTTS(text);
      return;
    } finally {
      setIsLoading(false);
    }
  };

  const checkAvatarStatus = async (jobId: string) => {
    try {
      const { getAvatarStatus } = await import("@/lib/avatar");
      const result = await getAvatarStatus(jobId);

      if (result.status === "done" && result.video_url) {
        setVideoUrl(result.video_url);
        setError(null);
        setIsIdle(false);
      } else if (result.status === "error") {
        setError("Avatar generation failed");
        setIsIdle(true); // Return to idle on error
      } else {
        // Still processing, check again in 2 seconds
        setTimeout(() => checkAvatarStatus(jobId), 2000);
      }
    } catch (err) {
      console.error("Failed to check avatar status:", err);
      setError("Failed to check avatar status");
    }
  };

  const handleVideoEnd = () => {
    // Keep the avatar visible after video ends (show last frame)
    // Don't return to idle - avatar stays on screen
  };

  // Cleanup speech on unmount
  useEffect(() => {
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  return (
    <div className="avatar-player">
      {isLoading && (
        <div className="avatar-loading">
          <div className="spinner-large"></div>
          <p>Generating avatar...</p>
        </div>
      )}

      {error && !isIdle && (
        <div className="avatar-error">
          <p>{error}</p>
        </div>
      )}

      {/* Idle image - shows when not speaking */}
      {isIdle && !isLoading && !isSpeaking && (
        <div className="avatar-idle-container">
          <img
            src="/avatar-idle.svg"
            alt="AI Interviewer"
            className="avatar-idle-image"
          />
          <div className="breathing-indicator"></div>
        </div>
      )}

      {/* Speaking with TTS - shows ChatGPT-style orb */}
      {isSpeaking && !videoUrl && (
        <div className="avatar-speaking-container">
          <div className="voice-orb-container">
            <div className="voice-orb">
              <div className="orb-core"></div>
              <div className="orb-ring orb-ring-1"></div>
              <div className="orb-ring orb-ring-2"></div>
              <div className="orb-ring orb-ring-3"></div>
            </div>
            <p className="speaking-text">AI Interviewer is speaking...</p>
          </div>
        </div>
      )}

      {/* Speaking video - plays when asking question and stays visible */}
      {videoUrl && (
        <video
          key="speaking"
          ref={videoRef}
          src={videoUrl}
          autoPlay
          playsInline
          className="avatar-video"
          onEnded={handleVideoEnd}
        />
      )}

      {!videoUrl && !isLoading && !error && !isIdle && (
        <div className="avatar-placeholder">
          <div className="avatar-icon">👤</div>
          <p>AI Interviewer</p>
        </div>
      )}
    </div>
  );
}
