from pydantic import BaseModel
from datetime import date
from typing import List, Optional


class SessionWord(BaseModel):
    word_id: int
    explanation_quiz: str
    correct_answer: str
    choices: List[str]
    audio_example_1: Optional[str] = None
    audio_example_2: Optional[str] = None

    class Config:
        from_attributes = True


class AnswerRequest(BaseModel):
    word_id: int
    correct: bool


class AnswerResponse(BaseModel):
    word_id: int
    correct: bool
    next_review_date: date
    new_interval: int

    class Config:
        from_attributes = True
