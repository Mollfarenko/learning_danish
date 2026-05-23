# backend/app/db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import time

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

DATABASE_URL = os.getenv("DATABASE_URL")

# Retry connection — PostgreSQL might not be ready yet
def create_engine_with_retry(url, retries=10, delay=2):
    for attempt in range(retries):
        try:
            engine = create_engine(url)
            # Test the connection
            with engine.connect() as conn:
                pass
            print("Database connected successfully!")
            return engine
        except Exception as e:
            if attempt < retries - 1:
                print(f"Database not ready, retrying in {delay}s... (attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                raise e

engine = create_engine_with_retry(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
