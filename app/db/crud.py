# app/db/crud.py

from sqlalchemy.orm import Session
from app.db.models import User
from telegram import User as TelegramUser

def get_or_create_user(db: Session, telegram_user: TelegramUser):
    """
    Получает пользователя из БД или создаёт нового по telegram_id.
    """
    user = db.query(User).filter(User.telegram_id == telegram_user.id).first()
    if not user:
        user = User(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name or ""
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user