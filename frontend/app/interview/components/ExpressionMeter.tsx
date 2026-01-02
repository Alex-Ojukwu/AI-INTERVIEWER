"use client";

interface ExpressionMeterProps {
  emotionData: any;
}

export default function ExpressionMeter({ emotionData }: ExpressionMeterProps) {
  if (!emotionData || !emotionData.face_detected) {
    return (
      <div className="expression-meter">
        <p className="no-face">No face detected</p>
      </div>
    );
  }

  const emotions = emotionData.emotions || {};
  const dominantEmotion = emotionData.dominant_emotion;
  const confidence = (emotionData.confidence * 100).toFixed(0);

  return (
    <div className="expression-meter">
      <div className="dominant-emotion">
        <span className="emotion-label">Current Expression:</span>
        <span className="emotion-value">{dominantEmotion}</span>
        <span className="confidence">({confidence}%)</span>
      </div>

      <div className="emotion-bars">
        {Object.entries(emotions).map(([emotion, value]: [string, any]) => (
          <div key={emotion} className="emotion-bar-container">
            <span className="emotion-name">{emotion}</span>
            <div className="emotion-bar-track">
              <div
                className="emotion-bar-fill"
                style={{ width: `${(value * 100).toFixed(0)}%` }}
              />
            </div>
            <span className="emotion-percent">
              {(value * 100).toFixed(0)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
