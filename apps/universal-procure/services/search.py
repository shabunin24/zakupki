import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime

from providers.api_open import APIOpenProvider
from providers.html_scraper import HTMLScraperProvider
from services.normalize import DataNormalizer
from services.cache import CacheService

class SearchService:
    """
    Основной сервис поиска закупок
    Объединяет работу с API и HTML скрейпингом
    """
    
    def __init__(self):
        self.api_provider = APIOpenProvider()
        self.scraper_provider = HTMLScraperProvider()
        self.normalizer = DataNormalizer()
        self.cache = CacheService()
    
    async def search(self, filters: Dict[str, Any], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Выполняет поиск закупок по фильтрам
        
        Args:
            filters: Словарь с фильтрами поиска
            limit: Максимальное количество результатов
            
        Returns:
            Список нормализованных закупок
        """
        # Проверяем кеш
        cache_key = self._generate_cache_key(filters, limit)
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Выполняем поиск через API
        api_results = []
        try:
            api_results = await self.api_provider.search(filters, limit)
        except Exception as e:
            print(f"Ошибка API провайдера: {e}")
        
        # Если API не дал результатов, пробуем скрейпинг
        if not api_results:
            try:
                scraper_results = await self.scraper_provider.search(filters, limit)
                if scraper_results:
                    api_results = scraper_results
            except Exception as e:
                print(f"Ошибка скрейпера: {e}")
        
        # Нормализуем результаты
        normalized_results = []
        for result in api_results:
            try:
                normalized = self.normalizer.normalize_purchase(result)
                if normalized:
                    normalized_results.append(normalized)
            except Exception as e:
                print(f"Ошибка нормализации закупки: {e}")
                continue
        
        # Кешируем результат
        if normalized_results:
            await self.cache.set(cache_key, normalized_results, ttl=300)  # 5 минут
        
        return normalized_results[:limit]
    
    def _generate_cache_key(self, filters: Dict[str, Any], limit: int) -> str:
        """Генерирует ключ кеша на основе фильтров и лимита"""
        import hashlib
        import json
        
        # Сортируем фильтры для стабильного ключа
        sorted_filters = dict(sorted(filters.items()))
        sorted_filters['limit'] = limit
        
        # Создаем JSON строку и хеш
        filters_str = json.dumps(sorted_filters, sort_keys=True, default=str)
        return f"search:{hashlib.md5(filters_str.encode()).hexdigest()}"
    
    async def search_by_text(self, text: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск по текстовому запросу
        
        Args:
            text: Текстовый запрос
            limit: Максимальное количество результатов
            
        Returns:
            Список закупок
        """
        filters = {"text": text}
        return await self.search(filters, limit)
    
    async def search_by_category(self, okpd2_codes: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск по категориям ОКПД2
        
        Args:
            okpd2_codes: Список кодов ОКПД2
            limit: Максимальное количество результатов
            
        Returns:
            Список закупок
        """
        filters = {"okpd2": okpd2_codes}
        return await self.search(filters, limit)
    
    async def search_by_region(self, regions: List[str], limit: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск по регионам
        
        Args:
            regions: Список регионов
            limit: Максимальное количество результатов
            
        Returns:
            Список закупок
        """
        filters = {"region": regions}
        return await self.search(filters, limit)
    
    async def search_by_price_range(self, min_price: Optional[float] = None, 
                                  max_price: Optional[float] = None, 
                                  limit: int = 20) -> List[Dict[str, Any]]:
        """
        Поиск по ценовому диапазону
        
        Args:
            min_price: Минимальная цена
            max_price: Максимальная цена
            limit: Максимальное количество результатов
            
        Returns:
            Список закупок
        """
        filters = {}
        if min_price is not None:
            filters["price_min"] = min_price
        if max_price is not None:
            filters["price_max"] = max_price
        
        return await self.search(filters, limit)
    
    async def get_purchase_details(self, purchase_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает детальную информацию о закупке
        
        Args:
            purchase_id: ID закупки
            
        Returns:
            Детали закупки или None
        """
        # Проверяем кеш
        cache_key = f"purchase:{purchase_id}"
        cached_result = await self.cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # Пытаемся получить детали через API
        try:
            # Здесь можно добавить логику получения деталей через API
            pass
        except Exception as e:
            print(f"Ошибка получения деталей через API: {e}")
        
        # Если API не сработал, пробуем скрейпинг
        try:
            # Извлекаем URL из ID
            if purchase_id.startswith("zakupki:"):
                purchase_url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={purchase_id.split(':')[1]}"
                details = await self.scraper_provider.get_purchase_details(purchase_url)
                if details:
                    # Кешируем результат
                    await self.cache.set(cache_key, details, ttl=600)  # 10 минут
                    return details
        except Exception as e:
            print(f"Ошибка получения деталей через скрейпинг: {e}")
        
        return None
