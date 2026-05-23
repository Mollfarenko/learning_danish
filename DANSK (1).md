# Dansk — Personal Danish Vocabulary App

## What is Dansk?

Dansk is a personalised Danish language learning app built for an English/Ukrainian speaker with no prior knowledge of Danish. It works like a smart flashcard system — you add Danish words you encounter, the app enriches them automatically using AI, generates high-quality audio pronunciations, and then you can study and practise them at your own pace.

---

## How it works

### Adding a word

You type any Danish word into the app — even with a typo or in an inflected form. The app sends it to OpenAI which:

- **Corrects typos** and returns two forms of the word:
  - **Inflected form** — the word as you intended it (e.g. *løber*)
  - **Base form** — the dictionary/infinitive form (e.g. *løbe*)
- **Explains the word in Danish** — a natural explanation in Danish
- **Explains the word in English** — so you understand it with zero Danish knowledge
- **Translates it** to English and Ukrainian directly
- **Generates 2 example sentences** in Danish, each translated into English and Ukrainian

All of this is stored in a PostgreSQL database so the OpenAI enrichment API is only called once per word.

### Audio pronunciation

After the word is enriched and saved, the app automatically generates **5 MP3 audio files** per word using the **OpenAI TTS API** (`tts-1-hd` model, Nova voice):

| Audio file | Content |
|---|---|
| `word_{id}_inflected.mp3` | Inflected form (e.g. *"Ordet er: løber"*) |
| `word_{id}_standardized.mp3` | Base form (e.g. *"Ordet er: løbe"*) |
| `word_{id}_explanation.mp3` | Full Danish explanation |
| `word_{id}_example1.mp3` | First Danish example sentence |
| `word_{id}_example2.mp3` | Second Danish example sentence |

The prefix *"Ordet er:"* ("The word is:") is added before word pronunciations to give Nova enough Danish context to pronounce correctly. Audio files are stored on disk in the `audio/` folder (Docker volume mounted) and served as static files by FastAPI. The TTS API is only called once at word creation — playback is always from stored files, no repeated API calls.

Audio is played in the browser using the **Web Audio API** with a gain boost (3x amplification) for clear volume on laptop speakers.

---

## Word card

Each word is displayed as a card showing:

| Element | Description |
|---|---|
| **Word** | The original input, with base form shown below if different |
| 🔊 **Word buttons** | One or two buttons to hear the word pronounced (inflected and/or base form) |
| **Danish explanation** | Natural explanation in Danish with a 🔊 button to hear it |
| **English explanation** | Same explanation in English (italic, no audio) |
| **Translations** | Direct translations to English and Ukrainian |
| **Examples** | 2 example sentences in Danish (with 🔊), English, and Ukrainian |

---

## Practising

The practice tab uses a **spaced repetition** system (SM-2 algorithm). You see a Danish quiz description of a word and must pick the correct base form from 5 choices. The app tracks your answers and schedules words for review based on how well you know them — words you struggle with appear more frequently, words you know well are spaced further apart.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| AI enrichment | OpenAI API (`gpt` chat completions) |
| AI pronunciation | OpenAI TTS API (`tts-1-hd`, Nova voice, 0.85x speed) |
| Audio storage | MP3 files on disk, Docker volume mounted |
| Frontend | Vanilla HTML/CSS/JS (single file) |
| Infrastructure | Docker, Docker Compose |
| Authentication | JWT tokens |

---

## Running the app

```bash
docker-compose up --build -d
```

Then create a user:
```bash
docker exec -it danskapp-app bash
python scripts/admin.py create-user you@example.com yourpassword
```

App runs at `http://localhost:8001`.

---

## Project structure

```
learning_danish/
├── backend/
│   └── app/
│       ├── models/        # SQLAlchemy DB models
│       ├── routers/       # FastAPI route handlers
│       ├── schemas/       # Pydantic API schemas
│       └── services/
│           ├── openai.py  # Word enrichment via OpenAI
│           ├── tts.py     # Audio generation via OpenAI TTS
│           ├── prompt.py  # LLM prompt for Danish enrichment
│           ├── sm2.py     # Spaced repetition algorithm
│           └── auth.py    # JWT authentication
├── frontend/
│   └── index.html         # Single-file frontend (all HTML/CSS/JS)
├── audio/                 # Generated MP3 files (Docker volume)
├── scripts/
│   └── admin.py           # CLI for user management
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## Environment variables

```
DB_PASSWORD=yourpassword
DATABASE_URL=postgresql://postgres:yourpassword@db:5432/danskapp
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```
