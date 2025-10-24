# run_bot.py — официальный, простой и надёжный

import os
import sys
import logging

# Настройка Ollama (важно для Windows)
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# Настройка путей
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from telegram.ext import Application
from app.core.config import settings
from app.bot.handlers import setup_handlers


def main():
    app = Application.builder().token(settings.telegram_bot_token).build()
    setup_handlers(app)
    print("🚀 Бот запущен! Нажмите Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()