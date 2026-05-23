from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List
import random

from ..db import get_db
from ..models.words import Word
from ..models.users import User
from ..models.review import Review
from ..services.sm2 import calculate_next_review
from ..services.auth import get_current_user
from ..schemas.practice_api import SessionWord, AnswerRequest, AnswerResponse

router = APIRouter()


@router.get("/session", response_model=List[SessionWord])
def get_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_words = db.query(Word).filter(Word.user_id == current_user.id).count()
    if total_words < 5:
        raise HTTPException(
            status_code=400,
            detail="You need at least 5 words in your library to start a practice session."
        )

    due_words = db.query(Word).outerjoin(Review).filter(
        Word.user_id == current_user.id,
        (Review.id == None) | (Review.next_review_date <= date.today())
    ).all()

    if not due_words:
        raise HTTPException(
            status_code=404,
            detail="No words due for review today. Come back tomorrow!"
        )

    all_words = db.query(Word).filter(Word.user_id == current_user.id).all()
    session = []

    for word in due_words:
        other_words = [w for w in all_words if w.id != word.id]
        if len(other_words) < 4:
            raise HTTPException(status_code=400, detail="You need at least 5 words in your library to start a practice session.")
        wrong_choices = random.sample(other_words, min(4, len(other_words)))

        choices = [w.standardized for w in wrong_choices] + [word.standardized]
        random.shuffle(choices)

        session.append(SessionWord(
            word_id=word.id,
            explanation_quiz=word.explanation_quiz,
            correct_answer=word.standardized,
            choices=choices,
        ))

    random.shuffle(session)
    return session


@router.post("/answer", response_model=AnswerResponse)
def submit_answer(
    answer: AnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(
        Word.id == answer.word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    review = db.query(Review).filter(Review.word_id == answer.word_id).first()

    if not review:
        review = Review(word_id=answer.word_id)
        db.add(review)
        db.flush()

    result = calculate_next_review(
        correct=answer.correct,
        repetitions=review.repetitions,
        interval=review.interval,
        easiness_factor=review.easiness_factor
    )

    review.interval = result["interval"]
    review.repetitions = result["repetitions"]
    review.easiness_factor = result["easiness_factor"]
    review.next_review_date = result["next_review_date"]

    db.commit()

    return AnswerResponse(
        word_id=answer.word_id,
        correct=answer.correct,
        next_review_date=result["next_review_date"],
        new_interval=result["interval"]
    )
