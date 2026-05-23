from pydantic import BaseModel
from datetime import date
from typing import List


# What the session endpoint returns — one question card
class SessionWord(BaseModel):
    word_id: int
    explanation_quiz: str
    correct_answer: str
    choices: List[str]

    class Config:
        from_attributes = True


# What the frontend sends when user clicks an answer
class AnswerRequest(BaseModel):
    word_id: int
    correct: bool


# What the server sends back after recording the answer
class AnswerResponse(BaseModel):
    word_id: int
    correct: bool
    next_review_date: date
    new_interval: int

    class Config:
        from_attributes = True
