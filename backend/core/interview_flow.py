"""
Interview Flow Module - Orchestrates the entire interview process
"""

import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from core.llm import InterviewLLM


class InterviewFlow:
    """
    Manages interview session state and flow
    Coordinates questions, answers, timing, and progression
    """

    def __init__(
        self,
        job_role: str,
        difficulty: str = "medium",
        duration_minutes: int = 30
    ):
        self.session_id = str(uuid.uuid4())
        self.job_role = job_role
        self.difficulty = difficulty
        self.duration_minutes = duration_minutes

        self.llm = InterviewLLM()

        # Interview state
        self.start_time = datetime.now()
        self.current_question_number = 0
        self.total_questions = self._calculate_total_questions()

        self.qa_pairs: List[Dict[str, str]] = []
        self.emotion_timeline: List[Dict] = []

        self.current_question: Optional[str] = None
        self.completed = False

    def _calculate_total_questions(self) -> int:
        """Calculate number of questions based on duration"""
        # Rough estimate: 3-5 minutes per question
        if self.duration_minutes <= 15:
            return 3
        elif self.duration_minutes <= 30:
            return 5
        else:
            return 7

    async def get_next_question(self) -> str:
        """
        Generate and return the next interview question

        Returns:
            Interview question text
        """
        self.current_question_number += 1

        # Build context from previous answers
        context = None
        if self.qa_pairs:
            recent_qa = self.qa_pairs[-2:]  # Last 2 Q&A pairs
            context = "\n".join([
                f"Q: {qa['question']}\nA: {qa['answer']}"
                for qa in recent_qa
            ])

        # Generate question
        question = await self.llm.generate_question(
            job_role=self.job_role,
            difficulty=self.difficulty,
            question_number=self.current_question_number,
            context=context
        )

        self.current_question = question
        return question

    async def process_answer(self, answer_text: str):
        """
        Process candidate's answer and store for evaluation

        Args:
            answer_text: Transcribed answer from candidate
        """
        if not self.current_question:
            raise ValueError("No active question to answer")

        # Store Q&A pair
        self.qa_pairs.append({
            "question": self.current_question,
            "answer": answer_text,
            "timestamp": datetime.now().isoformat(),
            "question_number": self.current_question_number
        })

        # Optionally evaluate answer
        evaluation = await self.llm.evaluate_answer(
            question=self.current_question,
            answer=answer_text,
            job_role=self.job_role
        )

        # Store evaluation
        self.qa_pairs[-1]["evaluation"] = evaluation

        # Clear current question
        self.current_question = None

    def add_emotion_data(self, emotion_data: Dict):
        """
        Add emotion analysis data point

        Args:
            emotion_data: Emotion metrics with timestamp
        """
        self.emotion_timeline.append({
            **emotion_data,
            "timestamp": datetime.now().isoformat()
        })

    def is_complete(self) -> bool:
        """Check if interview should end"""
        # Check question limit
        if self.current_question_number >= self.total_questions:
            self.completed = True
            return True

        # Check time limit
        elapsed = datetime.now() - self.start_time
        if elapsed > timedelta(minutes=self.duration_minutes):
            self.completed = True
            return True

        return False

    def get_elapsed_time(self) -> float:
        """Get elapsed time in minutes"""
        elapsed = datetime.now() - self.start_time
        return elapsed.total_seconds() / 60

    async def generate_summary(self) -> Dict[str, any]:
        """
        Generate final interview summary

        Returns:
            Comprehensive interview report
        """
        # Aggregate emotion data
        emotion_summary = self._aggregate_emotions()

        # Generate AI summary
        ai_summary = await self.llm.generate_summary(
            job_role=self.job_role,
            qa_pairs=self.qa_pairs,
            emotion_data=emotion_summary
        )

        return {
            "session_id": self.session_id,
            "job_role": self.job_role,
            "duration_minutes": self.get_elapsed_time(),
            "questions_asked": self.current_question_number,
            "qa_pairs": self.qa_pairs,
            "emotion_analysis": emotion_summary,
            "ai_assessment": ai_summary,
            "completed_at": datetime.now().isoformat()
        }

    def _aggregate_emotions(self) -> Dict[str, any]:
        """Aggregate emotion timeline into summary metrics"""
        if not self.emotion_timeline:
            return {}

        # Calculate average emotions
        emotion_counts = {}
        for data in self.emotion_timeline:
            dominant = data.get("dominant_emotion")
            if dominant:
                emotion_counts[dominant] = emotion_counts.get(dominant, 0) + 1

        total = len(self.emotion_timeline)
        emotion_percentages = {
            emotion: (count / total) * 100
            for emotion, count in emotion_counts.items()
        }

        return {
            "total_frames": total,
            "emotion_distribution": emotion_percentages,
            "most_common_emotion": max(emotion_counts, key=emotion_counts.get) if emotion_counts else None,
            "timeline": self.emotion_timeline[-10:]  # Last 10 data points
        }
