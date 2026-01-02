"use client";

import { useState, useEffect } from "react";
import WebcamFeed from "./components/WebcamFeed";
import AudioRecorder from "./components/AudioRecorder";
import AvatarPlayer from "./components/AvatarPlayer";
import ExpressionMeter from "./components/ExpressionMeter";
import ChatBox from "./components/ChatBox";
import Loader from "./components/Loader";
import { startInterview, submitAnswer } from "@/lib/api";
import "./styles.css";

export default function InterviewPage() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [interviewStatus, setInterviewStatus] = useState<"idle" | "active" | "completed">("idle");
  const [emotionData, setEmotionData] = useState<any>(null);
  const [questionNumber, setQuestionNumber] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(0);

  const handleStartInterview = async () => {
    setIsLoading(true);
    try {
      const response = await startInterview({
        job_role: "Software Engineer",
        difficulty: "medium",
        duration_minutes: 30,
      });

      setSessionId(response.session_id);
      setCurrentQuestion(response.question);
      setQuestionNumber(response.question_number);
      setTotalQuestions(response.total_questions);
      setInterviewStatus("active");
    } catch (error) {
      console.error("Failed to start interview:", error);
      alert("Failed to start interview. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswerSubmit = async (answerText: string) => {
    if (!sessionId) return;

    setIsLoading(true);
    try {
      const response = await submitAnswer(sessionId, answerText);

      if (response.status === "completed") {
        setInterviewStatus("completed");
        alert("Interview completed! Thank you.");
      } else {
        setCurrentQuestion(response.question);
        setQuestionNumber(response.question_number);
      }
    } catch (error) {
      console.error("Failed to submit answer:", error);
      alert("Failed to submit answer. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEmotionUpdate = (emotions: any) => {
    setEmotionData(emotions);
  };

  return (
    <div className="interview-container">
      <header className="interview-header">
        <h1>AI Virtual Interview Assistant</h1>
        {interviewStatus === "active" && (
          <p className="progress">
            Question {questionNumber} of {totalQuestions}
          </p>
        )}
      </header>

      {interviewStatus === "idle" && (
        <div className="start-screen">
          <h2>Welcome to Your AI Interview</h2>
          <p>Click the button below to begin your interview session.</p>
          <button
            onClick={handleStartInterview}
            disabled={isLoading}
            className="start-button"
          >
            {isLoading ? "Starting..." : "Start Interview"}
          </button>
        </div>
      )}

      {interviewStatus === "active" && (
        <div className="interview-active">
          <div className="video-section">
            <div className="avatar-container">
              <AvatarPlayer questionText={currentQuestion} />
            </div>

            <div className="webcam-container">
              <WebcamFeed onEmotionUpdate={handleEmotionUpdate} />
              <ExpressionMeter emotionData={emotionData} />
            </div>
          </div>

          <div className="interaction-section">
            <ChatBox question={currentQuestion} />
            <AudioRecorder
              onTranscriptionComplete={handleAnswerSubmit}
              disabled={isLoading}
            />
          </div>
        </div>
      )}

      {interviewStatus === "completed" && (
        <div className="completion-screen">
          <h2>Interview Completed!</h2>
          <p>Thank you for participating. Your results will be processed shortly.</p>
        </div>
      )}

      {isLoading && <Loader />}
    </div>
  );
}
