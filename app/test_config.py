# app/test_config.py
from core.config import settings

print("✅ Конфигурация загружена:")
print(f"  APP_NAME: {settings.app_name}")
print(f"  DEBUG: {settings.debug}")
print(f"  DATABASE_URL: {settings.database_url}")