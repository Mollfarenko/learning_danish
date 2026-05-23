from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    original = Column(String(100), nullable=False)
    standardized = Column(String(100), nullable=False)
    inflected = Column(String(100), nullable=False, default="")
    explanation = Column(Text, nullable=False)
    explanation_english = Column(Text, nullable=False, default="")
    translation_english = Column(Text, nullable=False, default="")
    translation_ukrainian = Column(Text, nullable=False, default="")
    explanation_quiz = Column(Text, nullable=False, default="")
    examples = Column(Text, nullable=False)
    audio_inflected = Column(String(200), nullable=True)
    audio_standardized = Column(String(200), nullable=True)
    audio_explanation = Column(String(200), nullable=True)
    audio_example_1 = Column(String(200), nullable=True)
    audio_example_2 = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review = relationship("Review", back_populates="word", uselist=False, passive_deletes=True)

