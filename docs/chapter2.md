# Chapter 2: Literature Review

## 2.1 Introduction

This chapter reviews existing research and technologies relevant to AI-powered virtual interviewing, facial emotion recognition, speech processing, and avatar generation.

## 2.2 AI in Recruitment and HR

### 2.2.1 Automated Interview Systems

Recent studies have explored the use of AI in recruitment:

- **HireVue** pioneered video interview analysis using computer vision and NLP
- **Pymetrics** uses neuroscience-based games and AI for candidate assessment
- Research by Campion et al. (2016) demonstrated that structured interviews increase validity and reduce bias

### 2.2.2 Conversational AI for Interviews

- GPT-3 and GPT-4 have shown capability in conducting natural conversations (Brown et al., 2020)
- Chatbot-based screening tools are increasingly used for initial candidate filtering
- Studies indicate candidates prefer AI interviews for reduced anxiety in initial rounds

## 2.3 Facial Expression and Emotion Recognition

### 2.3.1 Emotion Detection Technologies

Key technologies in emotion recognition:

**Deep Learning Approaches:**
- Convolutional Neural Networks (CNNs) for facial emotion recognition (Goodfellow et al., 2016)
- FER+ dataset contains 35,000+ labeled facial expressions
- State-of-the-art models achieve 70-85% accuracy on emotion classification

**Landmark-Based Methods:**
- Facial Action Coding System (FACS) - Ekman & Friesen (1978)
- MediaPipe Face Mesh provides 468 facial landmarks in real-time
- Suitable for resource-constrained environments

### 2.3.2 Emotion in Interview Context

Research findings on emotions in interviews:
- Nervous candidates may still be highly qualified (McCarthy & Goffin, 2004)
- Genuine emotional expression correlates with interview performance
- Cultural differences affect emotional expression interpretation

## 2.4 Speech Recognition and NLP

### 2.4.1 Automatic Speech Recognition (ASR)

Evolution of speech-to-text technology:

- Traditional systems: Hidden Markov Models (HMMs)
- Modern systems: Deep neural networks
- **OpenAI Whisper** (2022): Achieves human-level accuracy on diverse speech
  - Trained on 680,000 hours of multilingual data
  - Robust to accents, background noise, and technical jargon

### 2.4.2 Natural Language Understanding

NLP techniques for interview analysis:

- Sentiment analysis of candidate responses
- Keyword extraction for skill matching
- Answer relevance scoring
- Communication effectiveness metrics

## 2.5 Avatar Generation and Digital Humans

### 2.5.1 Talking Avatar Technologies

Recent advances in avatar generation:

**Text-to-Video Synthesis:**
- D-ID pioneered photorealistic talking avatars
- Wav2Lip for audio-driven facial animation
- Meta's EMO for realistic emotion expression

**Key Technologies:**
- Generative Adversarial Networks (GANs)
- Audio-to-viseme mapping
- Real-time facial reenactment

### 2.5.2 Human-Avatar Interaction

Research on human perception of avatars:

- Uncanny valley effect (Mori, 1970)
- Trust and credibility in avatar interactions
- Preference for expressive avatars over static images
- Effectiveness in professional contexts

## 2.6 System Architecture Approaches

### 2.6.1 Cloud vs. Local Processing

Trade-offs in AI system design:

**Cloud Processing:**
- Advantages: Unlimited compute, latest models, scalability
- Disadvantages: Latency, costs, privacy concerns, internet dependency

**Local Processing:**
- Advantages: Low latency, privacy, offline capability, no API costs
- Disadvantages: Hardware requirements, model size constraints

**Hybrid Approach:**
- Heavy AI operations (LLM, ASR) on cloud
- Real-time analysis (emotion) locally
- Optimal for resource-constrained environments

### 2.6.2 Real-Time Communication

WebSocket technology for real-time features:

- Enables bidirectional communication
- Lower latency than HTTP polling
- Suitable for video streaming and live analysis

## 2.7 Related Work and Existing Systems

### 2.7.1 Commercial Solutions

**HireVue:**
- Video interviewing platform with AI analysis
- Analyzes word choice, speaking patterns, facial expressions
- Used by 1000+ companies globally
- Criticism: Potential bias, lack of transparency

**Modern Hire:**
- Automated phone and video interviews
- Natural language processing for response analysis
- Integration with ATS systems

### 2.7.2 Academic Research Projects

Notable research projects:

1. **Automated Interview Agent** (MIT Media Lab)
   - Multimodal analysis of interview performance
   - Combines speech, vision, and physiological signals

2. **JobBot** (University of Cambridge)
   - Conversational agent for career counseling
   - Uses dialogue management and knowledge graphs

3. **EmotiW Challenge** (ACM ICMI)
   - Benchmark for emotion recognition in the wild
   - Multimodal emotion analysis from videos

## 2.8 Ethical Considerations

### 2.8.1 Bias and Fairness

Critical concerns in AI hiring:

- Algorithmic bias can perpetuate historical discrimination
- Need for diverse training data
- Regular auditing of AI decisions
- Transparency in evaluation criteria

### 2.8.2 Privacy and Data Protection

Data protection considerations:

- GDPR compliance for European candidates
- Video and audio data storage and retention
- Candidate consent and data rights
- Anonymization of sensitive information

## 2.9 Research Gap

Despite extensive research, gaps remain:

1. **Limited Integration**: Few systems combine conversational AI, emotion detection, and avatar interaction
2. **Hardware Constraints**: Most solutions require powerful hardware or full cloud dependency
3. **Hybrid Architectures**: Little research on optimal local-cloud distribution for interview systems
4. **Real-time Performance**: Challenge of maintaining low latency across multiple AI components
5. **Holistic Analysis**: Need for systems that combine verbal and non-verbal cues

This project addresses these gaps by implementing a comprehensive AI virtual interviewing system with hybrid architecture optimized for resource-constrained environments.

## 2.10 Summary

The literature review reveals:

- AI is increasingly viable for interview automation
- Emotion recognition technology has matured for practical use
- Modern speech recognition (Whisper) achieves high accuracy
- Avatar technology can create engaging interview experiences
- Hybrid architectures balance performance and resource constraints
- Ethical considerations are paramount in AI hiring systems

These findings inform the design and implementation of our AI Virtual Interview Assistant.

---

*Next: Chapter 3 - System Design and Architecture*
