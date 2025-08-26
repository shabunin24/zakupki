import asyncio
import json
import time
from typing import Any, Optional, Dict
from datetime import datetime, timedelta

class CacheService:
    """
    Сервис кеширования для поиска закупок
    Поддерживает Redis и in-memory кеш
    """
    
    def __init__(self, use_redis: bool = False, redis_url: str = "redis://localhost:6379"):
        self.use_redis = use_redis
        self.redis_url = redis_url
        self.redis_client = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        
        if use_redis:
            self._init_redis()
    
    def _init_redis(self):
        """Инициализация Redis клиента"""
        try:
            import redis.asyncio as redis
            self.redis_client = redis.from_url(self.redis_url)
        except ImportError:
            print("Redis не установлен, используется in-memory кеш")
            self.use_redis = False
        except Exception as e:
            print(f"Ошибка подключения к Redis: {e}, используется in-memory кеш")
            self.use_redis = False
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Получает значение из кеша
        
        Args:
            key: Ключ кеша
            
        Returns:
            Значение или None если не найдено
        """
        if self.use_redis and self.redis_client:
            try:
                value = await self.redis_client.get(key)
                if value:
                    return json.loads(value)
            except Exception as e:
                print(f"Ошибка получения из Redis: {e}")
        
        # Fallback к in-memory кешу
        return self._get_from_memory(key)
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """
        Устанавливает значение в кеш
        
        Args:
            key: Ключ кеша
            value: Значение для кеширования
            ttl: Время жизни в секундах
            
        Returns:
            True если успешно, False иначе
        """
        if self.use_redis and self.redis_client:
            try:
                await self.redis_client.setex(
                    key, 
                    ttl, 
                    json.dumps(value, default=str)
                )
                return True
            except Exception as e:
                print(f"Ошибка установки в Redis: {e}")
        
        # Fallback к in-memory кешу
        return self._set_to_memory(key, value, ttl)
    
    async def delete(self, key: str) -> bool:
        """
        Удаляет значение из кеша
        
        Args:
            key: Ключ кеша
            
        Returns:
            True если успешно, False иначе
        """
        if self.use_redis and self.redis_client:
            try:
                await self.redis_client.delete(key)
                return True
            except Exception as e:
                print(f"Ошибка удаления из Redis: {e}")
        
        # Fallback к in-memory кешу
        return self._delete_from_memory(key)
    
    async def clear(self) -> bool:
        """
        Очищает весь кеш
        
        Returns:
            True если успешно, False иначе
        """
        if self.use_redis and self.redis_client:
            try:
                await self.redis_client.flushdb()
                return True
            except Exception as e:
                print(f"Ошибка очистки Redis: {e}")
        
        # Fallback к in-memory кешу
        return self._clear_memory()
    
    def _get_from_memory(self, key: str) -> Optional[Any]:
        """Получает значение из in-memory кеша"""
        if key in self.memory_cache:
            cache_item = self.memory_cache[key]
            if cache_item["expires_at"] > datetime.now():
                return cache_item["value"]
            else:
                # Удаляем истекший элемент
                del self.memory_cache[key]
        return None
    
    def _set_to_memory(self, key: str, value: Any, ttl: int) -> bool:
        """Устанавливает значение в in-memory кеш"""
        try:
            expires_at = datetime.now() + timedelta(seconds=ttl)
            self.memory_cache[key] = {
                "value": value,
                "expires_at": expires_at
            }
            return True
        except Exception as e:
            print(f"Ошибка установки в memory кеш: {e}")
            return False
    
    def _delete_from_memory(self, key: str) -> bool:
        """Удаляет значение из in-memory кеша"""
        try:
            if key in self.memory_cache:
                del self.memory_cache[key]
            return True
        except Exception as e:
            print(f"Ошибка удаления из memory кеша: {e}")
            return False
    
    def _clear_memory(self) -> bool:
        """Очищает in-memory кеш"""
        try:
            self.memory_cache.clear()
            return True
        except Exception as e:
            print(f"Ошибка очистки memory кеша: {e}")
            return False
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Получает статистику кеша
        
        Returns:
            Словарь со статистикой
        """
        stats = {
            "type": "redis" if self.use_redis and self.redis_client else "memory",
            "memory_items": len(self.memory_cache),
            "memory_size_mb": 0
        }
        
        if self.use_redis and self.redis_client:
            try:
                stats["redis_info"] = await self.redis_client.info()
            except Exception as e:
                stats["redis_error"] = str(e)
        
        # Очищаем истекшие элементы из memory кеша
        current_time = datetime.now()
        expired_keys = [
            key for key, item in self.memory_cache.items()
            if item["expires_at"] <= current_time
        ]
        for key in expired_keys:
            del self.memory_cache[key]
        
        stats["memory_items_after_cleanup"] = len(self.memory_cache)
        
        return stats
    
    async def close(self):
        """Закрывает соединения"""
        if self.redis_client:
            try:
                await self.redis_client.close()
            except Exception as e:
                print(f"Ошибка закрытия Redis соединения: {e}")
