from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

@app.get("/")
async def root():
    return {"message": "🚀 Сервер запущен! Добро пожаловать в ПсихоАссистент!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

