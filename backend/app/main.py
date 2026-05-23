from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routers import word_routes, practice_routes, auth_routes
from .db import engine, Base
from .models import words, review, users # noqa — imported for SQLAlchemy table registration

import os
os.makedirs("audio", exist_ok=True)

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WordApp")

# CORS — allows your frontend (index.html) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this up later in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(word_routes.router, prefix="/words", tags=["words"])
app.include_router(practice_routes.router, prefix="/practice", tags=["practice"])

# Health check — useful for AWS and just confirming the server is alive
@app.get("/health")
def health():
    return {"status": "ok"}

# Serve audio files
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

# Serve frontend (catch-all — must be last)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
