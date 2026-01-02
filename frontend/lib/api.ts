/**
 * API Client - Functions to call FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface InterviewStartRequest {
  job_role: string;
  difficulty: string;
  duration_minutes: number;
  candidate_name?: string;
}

interface InterviewResponse {
  session_id: string;
  question: string;
  question_number: number;
  total_questions: number;
  status: string;
  summary?: any;
}

/**
 * Start a new interview session
 */
export async function startInterview(
  data: InterviewStartRequest
): Promise<InterviewResponse> {
  const response = await fetch(`${API_BASE_URL}/api/interview/start`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to start interview");
  }

  return response.json();
}

/**
 * Submit an answer and get the next question
 */
export async function submitAnswer(
  sessionId: string,
  answerText: string
): Promise<InterviewResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/interview/answer/${sessionId}`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ answer_text: answerText }),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to submit answer");
  }

  return response.json();
}

/**
 * Get interview session status
 */
export async function getInterviewStatus(sessionId: string): Promise<any> {
  const response = await fetch(
    `${API_BASE_URL}/api/interview/status/${sessionId}`
  );

  if (!response.ok) {
    throw new Error("Failed to get interview status");
  }

  return response.json();
}

/**
 * End interview session
 */
export async function endInterview(sessionId: string): Promise<any> {
  const response = await fetch(
    `${API_BASE_URL}/api/interview/end/${sessionId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to end interview");
  }

  return response.json();
}

/**
 * Transcribe audio file
 */
export async function transcribeAudio(audioData: FormData): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/audio/transcribe`, {
    method: "POST",
    body: audioData,
  });

  if (!response.ok) {
    throw new Error("Failed to transcribe audio");
  }

  return response.json();
}

/**
 * Analyze emotion from base64 image
 */
export async function analyzeEmotion(imageData: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/emotion/analyze-base64`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image: imageData.split(",")[1] }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyze emotion");
  }

  return response.json();
}

/**
 * Batch analyze emotions
 */
export async function batchAnalyzeEmotions(frames: any[]): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/emotion/batch-analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(frames),
  });

  if (!response.ok) {
    throw new Error("Failed to batch analyze emotions");
  }

  return response.json();
}
