import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.db.session import SessionLocal
from app.db.models import User, Message

db = SessionLocal()
users = db.query(User).all()
messages = db.query(Message).all()

print(f"\n👥 Найдено пользователей: {len(users)}")
for u in users:
    name = u.first_name or ""
    username = f"@{u.username}" if u.username else ""
    print(f"  - Telegram ID: {u.telegram_id}, Имя: {name} {username}")

print(f"\n💬 Всего сообщений: {len(messages)}")
for m in messages[-5:]:  # последние 5 сообщений
    text_preview = m.text[:60].replace("\n", " ")
    print(f"  - [{m.created_at.strftime('%Y-%m-%d %H:%M')}] {text_preview}...")

db.close()
print("\n✅ Проверка завершена.")
