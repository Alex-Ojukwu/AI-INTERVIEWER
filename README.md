# AI Virtual Interview Assistant

An intelligent virtual interview platform powered by AI, featuring real-time facial expression analysis, automated question generation, and talking avatar interaction.

## Overview

This Final Year Project implements an end-to-end AI-powered interview system that:

- Conducts automated interviews using GPT-4
- Analyzes candidate emotions in real-time using MediaPipe
- Features a talking AI avatar interviewer (D-ID)
- Transcribes responses using Whisper AI
- Generates comprehensive interview reports

## System Architecture

**Hybrid Local-Cloud Architecture:**

### Local Components (Your Laptop)
- Next.js frontend interface
- FastAPI backend server
- MediaPipe facial emotion detection
- Webcam and audio capture

### Cloud Services (APIs)
- OpenAI GPT-4 (interview logic)
- OpenAI Whisper (speech-to-text)
- D-ID API (talking avatar)

## Features

### Core Functionality
- AI-generated interview questions tailored to job role
- Real-time emotion and engagement tracking
- Speech-to-text transcription of answers
- Talking avatar with lip-sync and natural movements
- Comprehensive interview analytics and reports

### Technical Highlights
- WebSocket-based real-time communication
- Optimized for NVIDIA Quadro M1000M GPU
- REST API architecture
- TypeScript frontend with React
- Python backend with FastAPI

## Project Structure

```
project-root/
├── frontend/              # Next.js UI
│   ├── app/
│   │   └── interview/     # Main interview interface
│   └── lib/               # API clients and utilities
│
├── backend/               # Python FastAPI
│   ├── routers/           # API endpoints
│   ├── core/              # Business logic (LLM, Whisper)
│   ├── services/          # Face analysis, video streaming
│   ├── schemas/           # Pydantic models
│   └── models/            # ML models
│
├── cloud/                 # Cloud service configs
│   └── avatars/
│
└── docs/                  # FYP documentation
    ├── chapter1.md
    ├── chapter2.md
    ├── chapter3.md
    └── diagrams/
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (React)
- **Language**: TypeScript
- **Styling**: CSS
- **Real-time**: WebSockets

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **AI/ML**: OpenAI GPT-4, Whisper, MediaPipe
- **Computer Vision**: OpenCV, TensorFlow Lite

### Cloud Services
- **OpenAI API**: GPT-4, Whisper
- **D-ID API**: Avatar generation

## Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- NVIDIA GPU (for local emotion detection)
- Webcam and microphone

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Run the server:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment:
```bash
cp .env.local.example .env.local
# Edit if needed (default: localhost:8000)
```

4. Run development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## Usage

1. Start the backend server (port 8000)
2. Start the frontend development server (port 3000)
3. Navigate to `http://localhost:3000/interview`
4. Click "Start Interview"
5. Allow camera and microphone permissions
6. Answer questions by recording audio
7. View real-time emotion analysis
8. Complete interview and view summary

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Key API Endpoints

### Interview
- `POST /api/interview/start` - Start interview
- `POST /api/interview/answer/{session_id}` - Submit answer
- `GET /api/interview/status/{session_id}` - Get status
- `WS /api/interview/ws/{session_id}` - WebSocket connection

### Audio
- `POST /api/audio/transcribe` - Transcribe audio

### Emotion
- `POST /api/emotion/analyze` - Analyze emotion
- `POST /api/emotion/analyze-base64` - Analyze base64 image

### Avatar
- `POST /api/avatar/generate` - Generate avatar video

## Configuration

### Required API Keys

Add these to `backend/.env`:

```env
OPENAI_API_KEY=sk-...           # Required
DID_API_KEY=...                 # Optional (for avatar)
```

### Optional Settings

Adjust in `backend/config.py`:
- Interview duration
- Emotion confidence threshold
- Audio file size limits
- CORS origins

## Hardware Requirements

### Minimum
- Intel Core i5 or equivalent
- 8GB RAM
- NVIDIA GPU with 2GB VRAM
- Webcam and microphone

### Recommended
- Intel Core i7 or equivalent
- 16GB RAM
- NVIDIA GPU with 4GB+ VRAM
- HD webcam

## Development

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Type Checking
```bash
cd frontend
npm run type-check
```

### Code Formatting
```bash
# Backend
black backend/
flake8 backend/

# Frontend
npm run lint
```

## Troubleshooting

### Webcam Not Working
- Check browser permissions
- Ensure no other application is using the camera
- Try HTTPS (required by some browsers)

### Microphone Not Working
- Check browser permissions
- Test microphone in system settings
- Verify audio format support

### Backend Connection Failed
- Ensure backend is running on port 8000
- Check firewall settings
- Verify CORS configuration

### Emotion Detection Slow
- MediaPipe is optimized for your GPU
- Reduce webcam resolution in code
- Increase analysis interval (default: 2 seconds)

## Project Timeline

This project was developed as a Final Year Project for the 2024/2025 academic year.

**Development Phases:**
1. **Research & Planning** (2 weeks)
2. **Backend Development** (4 weeks)
3. **Frontend Development** (3 weeks)
4. **Integration & Testing** (2 weeks)
5. **Documentation** (1 week)

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Video recording and playback
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Interview templates for different roles
- [ ] Integration with HR systems

## Academic Context

**Course**: Final Year Project
**Department**: Computer Science
**Academic Year**: 2024/2025

**Key Research Areas:**
- Artificial Intelligence in HR
- Emotion Recognition
- Human-Computer Interaction
- Natural Language Processing

## License

This project is submitted as academic work for educational purposes.

## Acknowledgments

- OpenAI for GPT-4 and Whisper APIs
- D-ID for avatar generation technology
- MediaPipe team for facial analysis framework
- FastAPI and Next.js communities

## Contact

For questions or issues related to this project, please refer to the project documentation or contact the development team.

---

**Built with Python, TypeScript, AI, and dedication.**
