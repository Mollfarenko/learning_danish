from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..db import Base
from datetime import date

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False, unique=True)
    next_review_date = Column(Date, nullable=False, default=date.today)
    interval = Column(Integer, nullable=False, default=1)
    easiness_factor = Column(Float, nullable=False, default=2.5)
    repetitions = Column(Integer, nullable=False, default=0)

    word = relationship("Word", back_populates="review")
