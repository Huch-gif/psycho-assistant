from app.core.config import settings

print("✅ Токен:", settings.telegram_bot_token[:10] + "...")
print("✅ БД:", settings.database_url)
print("✅ Модель:", settings.ollama_model)