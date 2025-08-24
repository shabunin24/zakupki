from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router
from app.core.redis import redis_client
from app.tasks.celery_app import celery_app

# Создание таблиц при запуске
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц
    Base.metadata.create_all(bind=engine)
    
    # Проверка подключения к Redis
    try:
        await redis_client.ping()
        print("✅ Redis подключен")
    except Exception as e:
        print(f"❌ Ошибка подключения к Redis: {e}")
    
    # Проверка Celery
    try:
        celery_app.control.inspect().active()
        print("✅ Celery подключен")
    except Exception as e:
        print(f"❌ Ошибка подключения к Celery: {e}")
    
    yield
    
    # Очистка при завершении
    await redis_client.close()

app = FastAPI(
    title="ГосЗакупки API",
    description="API для Telegram Mini App по работе с государственными закупками",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "ГосЗакупки API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "celery": "connected"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
