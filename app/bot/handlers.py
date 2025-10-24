# app/bot/handlers.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy.orm import Session

# Импорты проекта
from app.db.database import SessionLocal
from app.db.crud import get_or_create_user
from app.db.models import User, Message, MoodLog
from app.bot.utils import is_crisis_message
from app.ai.client import get_ai_response

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Привет! 👋 Я — ПсихоАссистент.\n\n"
        "Я здесь, чтобы выслушать тебя и поддержать. "
        "Расскажи, что у тебя на душе?\n\n"
        "💡 Ты можешь:\n"
        "• Просто написать, как ты себя чувствуешь\n"
        "• Использовать команду /mood для оценки настроения"
    )


async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /mood"""
    await update.message.reply_text(
        "Хорошо! Давай оценим твоё настроение.\n\n"
        "Выбери эмоцию, которая ближе всего:\n"
        "тревога, грусть, усталость, злость, одиночество, "
        "спокойствие, радость, надежда, другое"
    )
    context.user_data["awaiting_mood"] = True


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обрабатывает все текстовые сообщения от пользователя.
    Поддерживает:
    - Состояния /mood (выбор эмоции → интенсивность)
    - Кризис-детекцию
    - Логирование в БД
    - Генерацию ответа от ИИ
    """
    telegram_user = update.effective_user
    user_text = update.message.text.strip()

    # === 1. Обработка состояния: ожидание эмоции (/mood) ===
    if context.user_data.get("awaiting_mood"):
        valid_moods = {
            "тревога", "грусть", "усталость", "злость", "одиночество",
            "спокойствие", "радость", "надежда", "другое"
        }
        mood_input = user_text.lower()
        mood = mood_input if mood_input in valid_moods else "другое"

        await update.message.reply_text(
            f"Ты выбрал: *{mood}*. По шкале от 1 (слабо) до 10 (очень сильно) — насколько это выражено?",
            parse_mode="Markdown"
        )
        context.user_data.update({
            "awaiting_intensity": True,
            "mood": mood
        })
        return

    # === 2. Обработка состояния: ожидание интенсивности (/mood) ===
    if context.user_data.get("awaiting_intensity"):
        try:
            intensity = int(user_text)
            if 1 <= intensity <= 10:
                db: Session = SessionLocal()
                try:
                    user = get_or_create_user(db, telegram_user)
                    log = MoodLog(user_id=user.id, mood=context.user_data["mood"], intensity=intensity)
                    db.add(log)
                    db.commit()
                    await update.message.reply_text(
                        f"💙 Спасибо! Твоё настроение «{context.user_data['mood']}» ({intensity}/10) сохранено.\n\n"
                        "Ты всегда можешь написать /mood снова."
                    )
                finally:
                    db.close()
            else:
                await update.message.reply_text("Пожалуйста, введи число от 1 до 10.")
                return
        except ValueError:
            await update.message.reply_text("Пожалуйста, введи число от 1 до 10.")
            return
        finally:
            # Очистка состояния в любом случае
            context.user_data.pop("awaiting_mood", None)
            context.user_data.pop("awaiting_intensity", None)
            context.user_data.pop("mood", None)
        return

    # === 3. ОСНОВНОЙ ПОТОК: обычные сообщения ===
    db: Session = SessionLocal()
    try:
        user = get_or_create_user(db, telegram_user)
        new_message = Message(user_id=user.id, text=user_text)
        db.add(new_message)
        db.commit()
        logger.info(f"Сообщение от пользователя {user.telegram_id} сохранено в БД")

        # 🚨 Кризис: мгновенный ответ
        if is_crisis_message(user_text):
            logger.warning(f"КРИЗИСНОЕ СООБЩЕНИЕ от {user.telegram_id}: {user_text}")
            await update.message.reply_text(
                "🚨 Ты не один. Пожалуйста, обратись за помощью прямо сейчас:\n\n"
                "• Телефон доверия (Россия): 8-800-2000-122 (бесплатно, 24/7)\n"
                "• Единый номер экстренных служб: 112\n\n"
                "Я рядом и слушаю тебя. Ты важен. ❤️"
            )
            return

        # ✨ Промежуточное сообщение
        processing_msg = await update.message.reply_text("🧠 Обрабатываю твой запрос...")

        # 🔍 Вызов ИИ (синхронный)
        try:
            logger.debug(f"Запрос к ИИ: {user_text}")
            ai_response = get_ai_response(user_text)
            logger.debug(f"Ответ от ИИ: {ai_response[:100]}...")
        except Exception as e:
            logger.error(f"❌ ОШИБКА В ИИ: {type(e).__name__}: {e}")
            ai_response = (
                "Спасибо, что поделился этим. Мне важно, чтобы ты знал: ты не один. "
                "Хочешь, поговорим об этом подробнее?"
            )

        # 📤 Отправка финального ответа
        await processing_msg.edit_text(ai_response)

    finally:
        db.close()


def setup_handlers(application):
    """
    Регистрирует все обработчики в приложении.
    """
    from telegram.ext import CommandHandler, MessageHandler, filters

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("mood", mood))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))