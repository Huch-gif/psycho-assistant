# check_env.py
from app.core.config import settings
print("✅ Telegram токен загружен:", settings.telegram_bot_token[:10] + "...")