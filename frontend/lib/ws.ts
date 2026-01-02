/**
 * WebSocket Client for real-time communication
 */

const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export class InterviewWebSocket {
  private ws: WebSocket | null = null;
  private sessionId: string;
  private messageHandlers: Map<string, (data: any) => void> = new Map();

  constructor(sessionId: string) {
    this.sessionId = sessionId;
  }

  /**
   * Connect to WebSocket server
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(
          `${WS_BASE_URL}/api/interview/ws/${this.sessionId}`
        );

        this.ws.onopen = () => {
          console.log("WebSocket connected");
          resolve();
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
          } catch (error) {
            console.error("Error parsing WebSocket message:", error);
          }
        };

        this.ws.onerror = (error) => {
          console.error("WebSocket error:", error);
          reject(error);
        };

        this.ws.onclose = () => {
          console.log("WebSocket disconnected");
        };
      } catch (error) {
        reject(error);
      }
    });
  }

  /**
   * Send message through WebSocket
   */
  send(type: string, data: any): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type, ...data }));
    } else {
      console.error("WebSocket not connected");
    }
  }

  /**
   * Send video frame for emotion analysis
   */
  sendVideoFrame(imageData: string): void {
    this.send("video_frame", { image: imageData });
  }

  /**
   * Send audio chunk
   */
  sendAudioChunk(audioData: string): void {
    this.send("audio_chunk", { audio: audioData });
  }

  /**
   * Send emotion data
   */
  sendEmotionData(emotions: any): void {
    this.send("emotion_data", emotions);
  }

  /**
   * Register message handler
   */
  on(messageType: string, handler: (data: any) => void): void {
    this.messageHandlers.set(messageType, handler);
  }

  /**
   * Remove message handler
   */
  off(messageType: string): void {
    this.messageHandlers.delete(messageType);
  }

  /**
   * Handle incoming message
   */
  private handleMessage(message: any): void {
    const handler = this.messageHandlers.get(message.type);

    if (handler) {
      handler(message.data);
    }
  }

  /**
   * Close WebSocket connection
   */
  disconnect(): void {
    if (this.ws) {
      this.send("stop_stream", {});
      this.ws.close();
      this.ws = null;
    }
  }

  /**
   * Check if WebSocket is connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}
