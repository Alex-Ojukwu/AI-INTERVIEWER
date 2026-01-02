"use client";

interface ChatBoxProps {
  question: string;
}

export default function ChatBox({ question }: ChatBoxProps) {
  return (
    <div className="chat-box">
      <div className="chat-header">
        <h3>Current Question</h3>
      </div>

      <div className="chat-content">
        {question ? (
          <div className="message interviewer-message">
            <div className="message-icon">🤖</div>
            <div className="message-text">{question}</div>
          </div>
        ) : (
          <div className="no-question">
            <p>Waiting for question...</p>
          </div>
        )}
      </div>

      <div className="chat-footer">
        <p className="hint">Click "Start Recording" below to answer</p>
      </div>
    </div>
  );
}
