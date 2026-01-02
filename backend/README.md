# AI Virtual Interview Assistant - Backend

FastAPI backend for the AI Virtual Interview Assistant application.

## Features

- **Interview Management**: Orchestrate interview sessions with AI-generated questions
- **Emotion Detection**: Real-time facial expression analysis using MediaPipe
- **Speech-to-Text**: Audio transcription via OpenAI Whisper API
- **Avatar Generation**: Talking avatar synthesis using D-ID API
- **WebSocket Support**: Real-time video streaming and analysis

## Tech Stack

- **Framework**: FastAPI
- **AI/ML**: OpenAI GPT-4, Whisper, MediaPipe
- **Computer Vision**: OpenCV, TensorFlow Lite
- **Real-time**: WebSockets

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- `OPENAI_API_KEY`: Your OpenAI API key
- `DID_API_KEY`: Your D-ID API key (optional)

### 3. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Interview

- `POST /api/interview/start` - Start new interview session
- `POST /api/interview/answer/{session_id}` - Submit answer
- `GET /api/interview/status/{session_id}` - Get interview status
- `DELETE /api/interview/end/{session_id}` - End interview
- `WS /api/interview/ws/{session_id}` - WebSocket connection

### Audio

- `POST /api/audio/transcribe` - Transcribe audio file

### Emotion

- `POST /api/emotion/analyze` - Analyze single image
- `POST /api/emotion/analyze-base64` - Analyze base64 image
- `POST /api/emotion/batch-analyze` - Batch analysis
- `GET /api/emotion/health` - Service health check

### Avatar

- `POST /api/avatar/generate` - Generate talking avatar
- `GET /api/avatar/status/{job_id}` - Check generation status
- `GET /api/avatar/voices` - List available voices
- `GET /api/avatar/presenters` - List available presenters

## Project Structure

```
backend/
├── main.py                 # FastAPI entry point
├── config.py              # Configuration management
├── routers/               # API route handlers
│   ├── interview.py
│   ├── audio.py
│   ├── emotion.py
│   └── avatar.py
├── core/                  # Core business logic
│   ├── llm.py            # OpenAI GPT integration
│   ├── whisper_api.py    # Whisper transcription
│   ├── interview_flow.py # Interview orchestration
│   └── utils.py          # Utility functions
├── services/             # External services
│   ├── face_analysis.py  # MediaPipe emotion detection
│   └── video_stream.py   # WebSocket video handler
├── schemas/              # Pydantic models
│   ├── interview.py
│   ├── emotion.py
│   └── avatar.py
└── models/               # ML models
    └── emotions_model.tflite
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
flake8 .
```

### Type Checking

```bash
mypy .
```

## Notes

- The emotion model uses MediaPipe for local processing (optimized for your GPU)
- Heavy AI operations (GPT, Whisper, Avatar) use cloud APIs
- WebSocket connections are used for real-time video streaming
- Audio files are temporarily stored and cleaned up after processing

## License

Final Year Project - 2024/2025
