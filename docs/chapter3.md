# Chapter 3: System Design and Architecture

## 3.1 Introduction

This chapter presents the system design and architecture of the AI Virtual Interview Assistant, including the rationale for the hybrid local-cloud approach, technology stack selection, and detailed component design.

## 3.2 System Requirements

### 3.2.1 Functional Requirements

**FR1: Interview Management**
- System shall initiate interview sessions based on job role and difficulty
- System shall generate contextually relevant interview questions
- System shall support 15-60 minute interview durations
- System shall handle multiple concurrent interview sessions

**FR2: Real-time Emotion Analysis**
- System shall capture video frames from candidate's webcam
- System shall detect facial expressions in real-time
- System shall identify emotions: neutral, happy, sad, angry, surprised, fearful, disgusted
- System shall aggregate emotion data over time

**FR3: Speech Processing**
- System shall record candidate's audio responses
- System shall transcribe speech to text using Whisper API
- System shall support audio formats: MP3, WAV, WebM, M4A
- System shall handle audio files up to 10MB

**FR4: Avatar Interaction**
- System shall generate talking avatar videos
- System shall synchronize lip movements with speech
- System shall support multiple avatar presenters and voices
- System shall display avatar to candidate during interview

**FR5: Interview Analytics**
- System shall evaluate candidate responses using AI
- System shall generate comprehensive interview reports
- System shall provide hiring recommendations
- System shall track engagement and emotional metrics

### 3.2.2 Non-Functional Requirements

**NFR1: Performance**
- Emotion detection latency < 500ms
- Avatar generation time < 30 seconds
- Speech transcription time < 5 seconds
- System shall support real-time video streaming at 15+ fps

**NFR2: Scalability**
- System shall support 50+ concurrent interviews
- System shall scale horizontally for increased load

**NFR3: Reliability**
- System availability: 99%
- Graceful degradation when cloud services fail
- Automatic session recovery after disconnection

**NFR4: Security**
- Secure storage of API keys
- HTTPS for all communications
- Candidate data encryption
- Session-based authentication

**NFR5: Usability**
- Intuitive user interface
- Browser-based (no installation required)
- Support for modern browsers: Chrome, Firefox, Safari, Edge

## 3.3 System Architecture

### 3.3.1 Hybrid Local-Cloud Architecture

Given hardware constraints (NVIDIA Quadro M1000M with 2GB VRAM), a hybrid architecture optimally distributes processing:

**Local Processing (Laptop):**
- Frontend user interface (Next.js)
- FastAPI backend server
- Facial emotion detection (MediaPipe + TFLite)
- WebSocket communication
- Webcam and audio capture

**Cloud Processing (APIs):**
- Interview conversation (OpenAI GPT-4)
- Speech transcription (OpenAI Whisper)
- Avatar generation (D-ID)

**Rationale:**

1. **Emotion Detection**: MediaPipe is optimized for CPU/lightweight GPU, runs efficiently on M1000M
2. **LLM Operations**: GPT-4 requires 100GB+ VRAM, impossible to run locally
3. **Speech Recognition**: Whisper Large requires 10GB+ VRAM, API is cost-effective
4. **Avatar Generation**: D-ID's models are proprietary and too large for local deployment

### 3.3.2 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Next.js Frontend (Port 3000)            │  │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────────────────┐  │  │
│  │  │ Webcam   │ │  Audio   │ │   Avatar Player     │  │  │
│  │  │  Feed    │ │ Recorder │ │                     │  │  │
│  │  └──────────┘ └──────────┘ └─────────────────────┘  │  │
│  │  ┌──────────────────┐ ┌─────────────────────────┐   │  │
│  │  │ Emotion Meter    │ │     Chat Box            │   │  │
│  │  └──────────────────┘ └─────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                │
│                            │ WebSocket + REST API           │
│                            ▼                                │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         FastAPI Backend (Port 8000) - LOCAL           │  │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────┐   │  │
│  │  │  Interview  │ │    Audio     │ │   Emotion    │   │  │
│  │  │   Router    │ │   Router     │ │   Router     │   │  │
│  │  └─────────────┘ └──────────────┘ └──────────────┘   │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │         MediaPipe Emotion Detection             │ │  │
│  │  │         (Local GPU Processing)                  │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS API Calls
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      CLOUD SERVICES                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  OpenAI API  │  │   Whisper    │  │    D-ID API     │   │
│  │   (GPT-4)    │  │     API      │  │  (Avatar Gen)   │   │
│  │              │  │              │  │                 │   │
│  │ - Question   │  │ - Speech to  │  │ - Talking       │   │
│  │   Generation │  │   Text       │  │   Avatar        │   │
│  │ - Answer     │  │ - Multi-     │  │ - Lip Sync      │   │
│  │   Evaluation │  │   lingual    │  │ - Voice         │   │
│  │ - Summary    │  │              │  │   Selection     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 3.3.3 Data Flow

**Interview Initiation Flow:**
1. User clicks "Start Interview" in frontend
2. Frontend sends POST request to `/api/interview/start`
3. Backend creates InterviewFlow instance
4. Backend calls GPT-4 API to generate first question
5. Backend returns question and session_id to frontend
6. Frontend requests avatar video from D-ID
7. Avatar video displays on screen

**Answer Submission Flow:**
1. User clicks "Record Answer"
2. Browser captures audio from microphone
3. Audio sent to `/api/audio/transcribe`
4. Backend forwards audio to Whisper API
5. Whisper returns transcribed text
6. Transcription sent to `/api/interview/answer/{session_id}`
7. Backend evaluates answer using GPT-4
8. Backend generates next question
9. Process repeats until interview complete

**Emotion Analysis Flow:**
1. Webcam captures video frames (15 fps)
2. JavaScript extracts frame as base64 image every 2 seconds
3. Frame sent to `/api/emotion/analyze-base64`
4. Backend decodes image
5. MediaPipe Face Mesh detects facial landmarks (LOCAL)
6. Emotion model classifies expression (LOCAL)
7. Emotion data returned to frontend
8. ExpressionMeter component updates UI
9. Emotion data aggregated for final report

## 3.4 Component Design

### 3.4.1 Frontend Components

**WebcamFeed Component:**
- Accesses user's webcam using WebRTC
- Captures frames at configurable intervals
- Sends frames to emotion analysis API
- Displays live video feed with "recording" indicator

**AudioRecorder Component:**
- Captures audio using MediaRecorder API
- Creates WebM audio blob
- Uploads to transcription endpoint
- Shows recording status and processing indicator

**AvatarPlayer Component:**
- Requests avatar video from backend
- Displays video with controls
- Handles loading states
- Falls back to placeholder if generation fails

**ExpressionMeter Component:**
- Visualizes detected emotions as progress bars
- Shows dominant emotion
- Displays confidence score
- Updates in real-time

**ChatBox Component:**
- Displays current interview question
- Shows interviewer avatar icon
- Clear, readable typography

### 3.4.2 Backend Components

**Interview Router (`routers/interview.py`):**
- Manages interview sessions (start, answer, status, end)
- WebSocket endpoint for real-time communication
- Session state management
- Question-answer flow coordination

**InterviewFlow (`core/interview_flow.py`):**
- Interview orchestration logic
- Tracks Q&A pairs, timing, progress
- Aggregates emotion data
- Generates final summary

**LLM Module (`core/llm.py`):**
- OpenAI GPT-4 integration
- Question generation with context
- Answer evaluation
- Summary generation
- Conversation history management

**Whisper API Module (`core/whisper_api.py`):**
- Audio transcription via OpenAI Whisper
- Supports multiple audio formats
- Timestamp extraction
- Confidence scoring

**Face Analyzer (`services/face_analysis.py`):**
- MediaPipe Face Mesh integration
- Real-time landmark detection
- Emotion classification (rule-based + ML)
- Aggregation of emotion timeline

**Video Stream Handler (`services/video_stream.py`):**
- WebSocket frame processing
- Base64 image encoding/decoding
- Frame optimization
- Real-time analysis pipeline

## 3.5 Database Design

**Note:** Current implementation uses in-memory storage for active sessions. For production, a database would store:

**Interview Sessions Table:**
- session_id (PK)
- candidate_name
- job_role
- difficulty
- start_time
- end_time
- status

**Questions Table:**
- question_id (PK)
- session_id (FK)
- question_text
- question_number
- timestamp

**Answers Table:**
- answer_id (PK)
- question_id (FK)
- answer_text
- audio_url
- evaluation_score
- timestamp

**Emotions Table:**
- emotion_id (PK)
- session_id (FK)
- timestamp
- dominant_emotion
- confidence
- emotion_distribution (JSON)

## 3.6 API Design

RESTful API endpoints follow these conventions:

**Naming:**
- Plural nouns for resources (`/interviews`, `/emotions`)
- Action verbs for operations (`/transcribe`, `/analyze`)
- Hierarchical structure (`/interview/{id}/answer`)

**HTTP Methods:**
- GET: Retrieve resources
- POST: Create resources
- PUT/PATCH: Update resources
- DELETE: Remove resources

**Response Format:**
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## 3.7 Security Design

**API Key Management:**
- Environment variables (`.env`)
- Never committed to version control
- Separate keys for development and production

**CORS Configuration:**
- Whitelist frontend origin only
- No wildcard (*) in production

**Session Security:**
- UUID-based session IDs
- Timeout after inactivity
- Session data cleaned up after completion

**File Upload Security:**
- File type validation
- Size limits enforced
- Temporary file cleanup
- No executable uploads allowed

## 3.8 Technology Justification

### 3.8.1 Why Next.js for Frontend?

- React-based for component reusability
- TypeScript support for type safety
- Built-in routing and API routes
- Excellent developer experience
- Good performance out-of-the-box

### 3.8.2 Why FastAPI for Backend?

- High performance (async support)
- Automatic API documentation (Swagger/ReDoc)
- Type hints with Pydantic
- WebSocket support
- Python ecosystem for AI/ML

### 3.8.3 Why MediaPipe for Emotion Detection?

- Optimized for low-end hardware
- Real-time performance on CPU/lightweight GPU
- Accurate facial landmark detection
- Cross-platform support
- Free and open-source

### 3.8.4 Why OpenAI APIs?

**GPT-4:**
- State-of-the-art language understanding
- Excellent context retention
- Natural conversation flow
- Requires no local GPU

**Whisper:**
- Near-human accuracy
- Robust to accents and noise
- Supports 99 languages
- Cost-effective for interviews

### 3.8.5 Why D-ID for Avatars?

- Photorealistic results
- Fast generation (< 30 seconds)
- Natural lip-sync
- Professional quality
- API-based (no local GPU needed)

## 3.9 Deployment Architecture

**Development Environment:**
- Frontend: `npm run dev` (localhost:3000)
- Backend: `python main.py` (localhost:8000)
- Local testing with development API keys

**Production Environment (Future):**
- Frontend: Vercel or Netlify
- Backend: AWS EC2 or Heroku
- Database: PostgreSQL
- File storage: AWS S3
- Monitoring: Sentry, CloudWatch

## 3.10 Summary

The system design addresses project requirements through:

1. **Hybrid Architecture**: Optimizes for hardware constraints
2. **Modular Design**: Separates concerns for maintainability
3. **Scalable APIs**: RESTful design for future growth
4. **Real-time Capabilities**: WebSockets for live features
5. **Security**: API key protection, CORS, input validation
6. **Technology Stack**: Modern, well-supported frameworks

This architecture enables efficient development while maintaining performance and scalability.

---

*Next: Chapter 4 - Implementation*
