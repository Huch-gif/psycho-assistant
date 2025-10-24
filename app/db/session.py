# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаём движок SQLite
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # важно для SQLite в многопоточности
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Зависимость для FastAPI (пока не используем, но полезно иметь)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()