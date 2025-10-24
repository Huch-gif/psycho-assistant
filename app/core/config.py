# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from pathlib import Path

# Определяем корень проекта (где лежит .env)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # Общие настройки
    app_name: str = "ПсихоАссистент"
    debug: bool = False
    secret_key: str = Field(
        default="insecure-default-key-change-in-production",
        description="Секретный ключ для подписи данных (заменить в продакшене!)"
    )

    # База данных
    database_url: str = Field(
        default=f"sqlite:///{BASE_DIR}/psycho.db",
        description="URL подключения к базе данных"
    )

    # Telegram
    telegram_bot_token: str = Field(
        ...,
        description="Токен Telegram-бота (обязательный, берётся из .env)"
    )

    # ИИ
    ollama_model: str = Field(
        default="llama3:latest",  # ← рекомендуется использовать полное имя
        description="Модель Ollama для генерации ответов"
    )

    # Настройки Pydantic v2
    model_config = {
        "env_file": BASE_DIR / ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "case_sensitive": False,
    }


# Создаём глобальный экземпляр с явным типом
settings: Settings = Settings()