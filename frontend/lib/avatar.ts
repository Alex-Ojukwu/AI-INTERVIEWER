/**
 * Avatar API Client - D-ID integration
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface AvatarRequest {
  text: string;
  voice_id?: string;
  presenter_id?: string;
}

interface AvatarResponse {
  video_url: string | null;
  duration: number | null;
  status: string;
  job_id: string | null;
}

/**
 * Generate talking avatar video
 */
export async function generateAvatar(
  text: string,
  voiceId: string = "en-US-JennyNeural",
  presenterId: string = "amy"
): Promise<AvatarResponse> {
  const response = await fetch(`${API_BASE_URL}/api/avatar/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      voice_id: voiceId,
      presenter_id: presenterId,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to generate avatar");
  }

  return response.json();
}

/**
 * Check avatar generation status
 */
export async function getAvatarStatus(jobId: string): Promise<AvatarResponse> {
  const response = await fetch(`${API_BASE_URL}/api/avatar/status/${jobId}`);

  if (!response.ok) {
    throw new Error("Failed to get avatar status");
  }

  return response.json();
}

/**
 * Get available voices
 */
export async function getAvailableVoices(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/avatar/voices`);

  if (!response.ok) {
    throw new Error("Failed to get voices");
  }

  return response.json();
}

/**
 * Get available presenters
 */
export async function getAvailablePresenters(): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/avatar/presenters`);

  if (!response.ok) {
    throw new Error("Failed to get presenters");
  }

  return response.json();
}
