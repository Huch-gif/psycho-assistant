# init_db.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from app.db.session import engine
from app.db.base import Base

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("✅ База обновлена с поддержкой /mood")