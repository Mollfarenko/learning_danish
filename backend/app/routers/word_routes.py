from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models.words import Word
from ..models.users import User
from ..schemas.word_api import WordCreate, WordResponse
from ..services.openai import enrich_word
from ..services.auth import get_current_user
from ..services.tts import generate_audio

router = APIRouter()

@router.post("/", response_model=WordResponse)
def add_word(
    word_data: WordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Word).filter(
        Word.original == word_data.original,
        Word.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Word already exists")

    try:
        enriched = enrich_word(word_data.original)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")

    new_word = Word(
        user_id=current_user.id,
        original=word_data.original,
        standardized=enriched["standardized"],
        inflected=enriched["inflected"],
        explanation=enriched["explanation"],
        explanation_english=enriched["explanation_english"],
        translation_english=enriched["translation_english"],
        translation_ukrainian=enriched["translation_ukrainian"],
        explanation_quiz=enriched["explanation_quiz"],
        examples=enriched["examples"]
    )

    db.add(new_word)
    db.commit()
    db.refresh(new_word)

    # Extract Danish example sentences for TTS
    danish_examples = [
        line.split("]: ", 1)[1].strip()
        for line in enriched["examples"].split("\n")
        if line.startswith("Example") and "[danish]" in line.lower()
    ]

    # Use prefix only for TTS, not stored in DB
    word_id = new_word.id
    new_word.audio_inflected = generate_audio(f"Ordet er: {enriched['inflected']}", f"word_{word_id}_inflected.mp3")
    new_word.audio_standardized = generate_audio(f"Ordet er: {enriched['standardized']}", f"word_{word_id}_standardized.mp3")
    new_word.audio_explanation = generate_audio(enriched["explanation"], f"word_{word_id}_explanation.mp3")
    new_word.audio_example_1 = generate_audio(danish_examples[0] if len(danish_examples) > 0 else "", f"word_{word_id}_example1.mp3")
    new_word.audio_example_2 = generate_audio(danish_examples[1] if len(danish_examples) > 1 else "", f"word_{word_id}_example2.mp3")


    db.commit()
    db.refresh(new_word)
    return new_word


@router.get("/", response_model=list[WordResponse])
def get_words(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    words = db.query(Word).filter(
        Word.user_id == current_user.id
    ).order_by(Word.created_at.desc()).all()
    return words


@router.get("/{word_id}", response_model=WordResponse)
def get_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@router.delete("/{word_id}")
def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.user_id == current_user.id
    ).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    db.delete(word)
    db.commit()
    return {"message": f"Word '{word.original}' deleted"}
