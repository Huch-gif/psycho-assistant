# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Создаём единый базовый класс для моделей
Base = declarative_base()

# Создаём движок базы данных
# Для SQLite (разработка):
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # требуется только для SQLite
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)