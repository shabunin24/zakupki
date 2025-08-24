from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "ГосЗакупки API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # База данных
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/zakupki_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_DB: int = 0
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Парсеры
    PARSER_INTERVAL_MINUTES: int = 15
    MAX_CONCURRENT_PARSERS: int = 5
    
    # Логирование
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Создание экземпляра настроек
settings = Settings()

# Создание .env файла если его нет
def create_env_file():
    env_content = """# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/zakupki_db

# Redis
REDIS_URL=redis://localhost:6379
REDIS_DB=0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook

# Безопасность
SECRET_KEY=your-secret-key-here

# Парсеры
PARSER_INTERVAL_MINUTES=15
MAX_CONCURRENT_PARSERS=5
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Создан файл .env с настройками по умолчанию")

# Создание .env файла при импорте
create_env_file()
