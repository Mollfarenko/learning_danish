# backend/app/services/tts.py

import os
import time
import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AUDIO_DIR = "/app/audio"
TTS_URL = "https://api.openai.com/v1/audio/speech"


def generate_audio(text: str, filename: str, retries: int = 2) -> str | None:
    """
    Calls OpenAI TTS API and saves the audio as an MP3 file.
    Retries on failure. Returns the relative path or None.
    """
    if not text or not text.strip():
        return None

    os.makedirs(AUDIO_DIR, exist_ok=True)
    filepath = os.path.join(AUDIO_DIR, filename)

    for attempt in range(retries):
        try:
            response = httpx.post(
                TTS_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "tts-1-hd",
                    "input": text,
                    "voice": "nova",
                    "response_format": "mp3",
                    "speed": 0.85,
                },
                timeout=60.0,
            )
            response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(response.content)

            time.sleep(0.3)  # small delay between calls to avoid rate limits
            return f"/audio/{filename}"

        except Exception as e:
            print(f"TTS attempt {attempt + 1} failed for '{filename}': {e}")
            if attempt < retries - 1:
                time.sleep(1.5)  # wait before retry

    return None
