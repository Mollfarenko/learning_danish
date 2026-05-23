from pydantic import BaseModel
from datetime import datetime

class WordCreate(BaseModel):
    original: str

class WordResponse(BaseModel):
    id: int
    original: str
    standardized: str
    inflected: str
    explanation: str
    explanation_english: str
    translation_english: str
    translation_ukrainian: str
    explanation_quiz: str
    examples: str
    audio_inflected: str | None = None
    audio_standardized: str | None = None
    audio_explanation: str | None = None
    audio_example_1: str | None = None
    audio_example_2: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
