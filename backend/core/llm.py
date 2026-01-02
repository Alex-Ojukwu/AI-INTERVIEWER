"""
LLM Module - OpenAI GPT API integration for interview conversations
"""

from openai import AsyncOpenAI
from typing import List, Dict, Optional
import json

from config import settings


class InterviewLLM:
    """
    Handles AI-powered interview conversation using OpenAI GPT
    Manages question generation, answer evaluation, and follow-ups
    """

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.conversation_history: List[Dict[str, str]] = []

    async def generate_question(
        self,
        job_role: str,
        difficulty: str,
        question_number: int,
        context: Optional[str] = None
    ) -> str:
        """
        Generate interview question based on role and context

        Args:
            job_role: Target job position
            difficulty: easy/medium/hard
            question_number: Current question number
            context: Previous answers context

        Returns:
            Generated interview question
        """
        system_prompt = f"""You are an expert interviewer conducting a {difficulty} level interview
        for a {job_role} position. Generate thoughtful, relevant interview questions that assess
        both technical skills and behavioral competencies. Be professional and encouraging."""

        user_prompt = f"Generate question #{question_number} for the interview."
        if context:
            user_prompt += f"\n\nContext from previous answers:\n{context}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )

            question = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": question})

            return question

        except Exception as e:
            print(f"Error generating question: {str(e)}")
            return "Can you tell me about your experience and background?"

    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        job_role: str
    ) -> Dict[str, any]:
        """
        Evaluate candidate's answer using AI

        Args:
            question: The interview question
            answer: Candidate's response
            job_role: Target position

        Returns:
            Evaluation with score, feedback, and analysis
        """
        prompt = f"""Evaluate this interview answer for a {job_role} position.

Question: {question}
Answer: {answer}

Provide:
1. Score (0-10)
2. Brief feedback
3. Key strengths
4. Areas for improvement

Format as JSON."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert interviewer providing constructive feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )

            result = response.choices[0].message.content.strip()

            # Try to parse as JSON, fallback to text
            try:
                evaluation = json.loads(result)
            except:
                evaluation = {
                    "score": 7,
                    "feedback": result,
                    "strengths": [],
                    "improvements": []
                }

            return evaluation

        except Exception as e:
            print(f"Error evaluating answer: {str(e)}")
            return {
                "score": 5,
                "feedback": "Unable to evaluate answer at this time.",
                "strengths": [],
                "improvements": []
            }

    async def generate_followup(
        self,
        original_question: str,
        answer: str
    ) -> Optional[str]:
        """
        Generate intelligent follow-up question based on answer

        Args:
            original_question: Previous question
            answer: Candidate's answer

        Returns:
            Follow-up question or None
        """
        prompt = f"""Based on this interview exchange, generate a relevant follow-up question:

Q: {original_question}
A: {answer}

Follow-up (or say "NONE" if no follow-up needed):"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=100
            )

            followup = response.choices[0].message.content.strip()

            if "NONE" in followup.upper():
                return None

            return followup

        except Exception as e:
            print(f"Error generating follow-up: {str(e)}")
            return None

    async def generate_summary(
        self,
        job_role: str,
        qa_pairs: List[Dict[str, str]],
        emotion_data: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Generate comprehensive interview summary

        Args:
            job_role: Position interviewed for
            qa_pairs: List of questions and answers
            emotion_data: Aggregated emotion metrics

        Returns:
            Interview summary with recommendation
        """
        qa_text = "\n\n".join([
            f"Q: {qa['question']}\nA: {qa['answer']}"
            for qa in qa_pairs
        ])

        emotion_context = ""
        if emotion_data:
            emotion_context = f"\n\nEmotional Analysis:\n{json.dumps(emotion_data, indent=2)}"

        prompt = f"""Generate a comprehensive interview summary for a {job_role} candidate.

Interview Transcript:
{qa_text}
{emotion_context}

Provide:
1. Overall assessment
2. Key strengths
3. Areas of concern
4. Hiring recommendation (Strong Yes/Yes/Maybe/No)
5. Overall score (0-100)

Format as JSON."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR interviewer providing hiring assessments."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
            )

            result = response.choices[0].message.content.strip()

            try:
                summary = json.loads(result)
            except:
                summary = {
                    "assessment": result,
                    "recommendation": "Review Required",
                    "score": 50
                }

            return summary

        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return {
                "assessment": "Unable to generate summary",
                "recommendation": "Manual Review Required",
                "score": 0
            }

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
