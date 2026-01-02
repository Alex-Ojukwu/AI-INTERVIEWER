/**
 * Audio Recording Utilities
 */

/**
 * Start audio recording
 */
export async function startRecording(): Promise<MediaRecorder> {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mediaRecorder = new MediaRecorder(stream, {
      mimeType: "audio/webm",
    });

    mediaRecorder.start();

    return mediaRecorder;
  } catch (error) {
    console.error("Error starting recording:", error);
    throw new Error("Unable to access microphone. Please check permissions.");
  }
}

/**
 * Stop audio recording
 */
export function stopRecording(mediaRecorder: MediaRecorder): void {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();

    // Stop all tracks
    mediaRecorder.stream.getTracks().forEach((track) => track.stop());
  }
}

/**
 * Convert audio blob to base64
 */
export function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onloadend = () => {
      if (typeof reader.result === "string") {
        resolve(reader.result);
      } else {
        reject(new Error("Failed to convert blob to base64"));
      }
    };

    reader.onerror = reject;

    reader.readAsDataURL(blob);
  });
}

/**
 * Download audio as file (for debugging)
 */
export function downloadAudio(audioBlob: Blob, filename: string = "recording.webm"): void {
  const url = URL.createObjectURL(audioBlob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
