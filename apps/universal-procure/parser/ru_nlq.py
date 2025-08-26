import re
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta

class NLQParser:
    """
    Парсер естественного языка для русских запросов о закупках
    """
    
    def __init__(self):
        self.okpd2_dict = self._load_okpd2_dict()
        self.regions_dict = self._load_regions_dict()
        self.methods_dict = self._load_methods_dict()
        self.statuses_dict = self._load_statuses_dict()
        
        # Русские суффиксы для лемматизации
        self.russian_suffixes = [
            "ов", "ые", "ие", "ий", "ая", "ой", "ы", "а", "я", "е", "у",
            "ом", "ем", "ой", "ей", "ью", "ью", "ами", "ями", "ах", "ях"
        ]
    
    def _load_okpd2_dict(self) -> Dict[str, List[str]]:
        """Загрузка справочника ОКПД2"""
        try:
            data_path = Path(__file__).parent.parent / "data" / "okpd2_dict.json"
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _load_regions_dict(self) -> List[Dict[str, Any]]:
        """Загрузка справочника регионов"""
        try:
            data_path = Path(__file__).parent.parent / "data" / "regions.json"
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _load_methods_dict(self) -> Dict[str, List[str]]:
        """Загрузка справочника методов закупки"""
        try:
            data_path = Path(__file__).parent.parent / "data" / "methods.json"
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _load_statuses_dict(self) -> Dict[str, List[str]]:
        """Загрузка справочника статусов"""
        try:
            data_path = Path(__file__).parent.parent / "data" / "statuses.json"
            if data_path.exists():
                with open(data_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _normalize_text(self, text: str) -> str:
        """Нормализация текста: нижний регистр, удаление пунктуации"""
        # Приводим к нижнему регистру
        text = text.lower()
        # Убираем лишние пробелы
        text = re.sub(r'\s+', ' ', text)
        # Убираем пунктуацию, оставляем только буквы, цифры и пробелы
        text = re.sub(r'[^\w\s]', ' ', text)
        return text.strip()
    
    def _lemmatize_word(self, word: str) -> str:
        """Простая лемматизация: удаление русских суффиксов"""
        if len(word) < 4:  # Слишком короткие слова не лемматизируем
            return word
        
        # Менее агрессивная лемматизация
        for suffix in self.russian_suffixes:
            if word.endswith(suffix) and len(word) - len(suffix) >= 4:
                word = word[:-len(suffix)]
                break
        
        return word
    
    def _lemmatize_text(self, text: str) -> str:
        """Лемматизация всего текста"""
        words = text.split()
        lemmatized_words = [self._lemmatize_word(word) for word in words]
        return ' '.join(lemmatized_words)
    
    def parse(self, query: str) -> Dict[str, Any]:
        """
        Парсит естественный языковой запрос в структурированные фильтры
        
        Args:
            query: Запрос на русском языке
            
        Returns:
            Словарь с фильтрами и диагностикой
        """
        original_query = query
        normalized_query = self._normalize_text(query)
        lemmatized_query = self._lemmatize_text(normalized_query)
        
        filters = {
            "text": original_query,
            "okpd2": [],
            "region": [],
            "price_min": None,
            "price_max": None,
            "method": [],
            "status": [],
            "publish_date_from": None,
            "publish_date_to": None,
            "deadline_from": None,
            "deadline_to": None
        }
        
        # Диагностика
        diagnostics = {
            "matched_keywords": [],
            "matched_okpd2": [],
            "regions_detected": [],
            "method_detected": None,
            "status_detected": None,
            "price_min": None,
            "price_max": None,
            "date_rules": []
        }
        
        # Извлекаем категории товаров/услуг
        okpd2_result = self._extract_categories(lemmatized_query)
        filters["okpd2"] = okpd2_result["codes"]
        diagnostics["matched_keywords"] = okpd2_result["keywords"]
        diagnostics["matched_okpd2"] = okpd2_result["codes"]
        
        # Извлекаем регионы (используем нормализованный текст)
        regions_result = self._extract_regions(normalized_query)
        filters["region"] = regions_result["regions"]
        diagnostics["regions_detected"] = regions_result["regions"]
        
        # Извлекаем ценовые диапазоны
        price_result = self._extract_price_range(lemmatized_query)
        if price_result:
            filters["price_min"] = price_result.get("min")
            filters["price_max"] = price_result.get("max")
            diagnostics["price_min"] = price_result.get("min")
            diagnostics["price_max"] = price_result.get("max")
        
        # Извлекаем методы закупки
        methods_result = self._extract_methods(lemmatized_query)
        filters["method"] = methods_result["methods"]
        diagnostics["method_detected"] = methods_result["methods"][0] if methods_result["methods"] else None
        
        # Извлекаем статусы
        statuses_result = self._extract_statuses(lemmatized_query)
        filters["status"] = statuses_result["statuses"]
        diagnostics["status_detected"] = statuses_result["statuses"][0] if statuses_result["statuses"] else None
        
        # Извлекаем временные рамки
        date_result = self._extract_date_range(lemmatized_query)
        if date_result:
            filters["publish_date_from"] = date_result.get("publish_from")
            filters["publish_date_to"] = date_result.get("publish_to")
            filters["deadline_from"] = date_result.get("deadline_from")
            filters["deadline_to"] = date_result.get("deadline_to")
            diagnostics["date_rules"] = date_result.get("rules", [])
        
        # Добавляем диагностику в результат
        filters["diagnostics"] = diagnostics
        
        return filters
    
    def _extract_categories(self, query: str) -> Dict[str, Any]:
        """Извлекает категории товаров/услуг по ключевым словам"""
        matched_keywords = []
        matched_codes = []
        
        # Ищем точные совпадения (сначала без лемматизации)
        for keyword, okpd2_codes in self.okpd2_dict.items():
            if keyword in query:
                matched_keywords.append(keyword)
                matched_codes.extend(okpd2_codes)
        
        # Если не нашли, пробуем с лемматизацией
        if not matched_keywords:
            for keyword, okpd2_codes in self.okpd2_dict.items():
                # Лемматизируем ключевое слово
                lemmatized_keyword = self._lemmatize_text(keyword)
                if lemmatized_keyword in query:
                    matched_keywords.append(keyword)
                    matched_codes.extend(okpd2_codes)
        
        # Если все еще не нашли, пробуем поиск по частям
        if not matched_keywords:
            query_words = set(query.split())
            for keyword, okpd2_codes in self.okpd2_dict.items():
                keyword_words = keyword.split()
                # Проверяем, есть ли все слова ключевого слова в запросе
                if all(word in query_words for word in keyword_words):
                    matched_keywords.append(keyword)
                    matched_codes.extend(okpd2_codes)
        
        # Убираем дубликаты и нормализуем коды
        matched_codes = list(set(matched_codes))
        
        # Если много кодов, укорачиваем к префиксам
        if len(matched_codes) > 10:
            # Группируем по префиксам
            prefix_groups = {}
            for code in matched_codes:
                if '*' in code:
                    prefix = code.replace('*', '')
                else:
                    parts = code.split('.')
                    if len(parts) >= 2:
                        prefix = '.'.join(parts[:2]) + '.*'
                    else:
                        prefix = code
                
                if prefix not in prefix_groups:
                    prefix_groups[prefix] = []
                prefix_groups[prefix].append(code)
            
            # Выбираем наиболее общие префиксы
            matched_codes = list(prefix_groups.keys())
        
        return {
            "keywords": matched_keywords,
            "codes": matched_codes
        }
    
    def _extract_regions(self, query: str) -> Dict[str, Any]:
        """Извлекает регионы из запросе"""
        detected_regions = []
        
        # Собираем все возможные совпадения с их длиной
        region_matches = []
        
        for region_info in self.regions_dict:
            canonical = region_info["canonical"]
            aliases = region_info["aliases"]
            
            # Проверяем каноническое название
            if canonical.lower() in query:
                match_length = len(canonical.lower())
                region_matches.append((canonical, match_length, "Город" in canonical))
                continue
            
            # Проверяем синонимы
            for alias in aliases:
                if alias.lower() in query:
                    match_length = len(alias.lower())
                    region_matches.append((canonical, match_length, "Город" in canonical))
                    break
        
        # Сортируем по длине совпадения (более длинные сначала) и приоритету города
        region_matches.sort(key=lambda x: (x[2], x[1]), reverse=True)
        
        # Берем первое совпадение (самое приоритетное)
        if region_matches:
            detected_regions = [region_matches[0][0]]
        
        return {"regions": detected_regions}
    
    def _extract_price_range(self, query: str) -> Optional[Dict[str, float]]:
        """Извлекает ценовой диапазон из запроса"""
        # Паттерны для цен
        price_patterns = [
            r'до\s+(\d+(?:\.\d+)?)\s*(?:тыс|тысяч|млн|миллион|руб|₽)',
            r'от\s+(\d+(?:\.\d+)?)\s*(?:тыс|тысяч|млн|миллион|руб|₽)',
            r'(\d+(?:\.\d+)?)\s*(?:тыс|тысяч|млн|миллион|руб|₽)',
            r'(\d+(?:\.\d+)?)\s*млн',
            r'(\d+(?:\.\d+)?)\s*тыс'
        ]
        
        price_range = {"min": None, "max": None}
        
        for pattern in price_patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                value = float(match)
                
                # Определяем единицы измерения
                if "млн" in query or "миллион" in query:
                    value *= 1000000
                elif "тыс" in query or "тысяч" in query:
                    value *= 1000
                
                # Определяем тип (до/от)
                if "до" in query:
                    price_range["max"] = value
                elif "от" in query:
                    price_range["min"] = value
                else:
                    # Если не указано "до" или "от", считаем максимальной ценой
                    if price_range["max"] is None or value > price_range["max"]:
                        price_range["max"] = value
        
        # Если указан диапазон "от X до Y"
        range_pattern = r'от\s+(\d+(?:\.\d+)?)\s*(?:тыс|тысяч|млн|миллион|руб|₽)?\s*до\s+(\d+(?:\.\d+)?)\s*(?:тыс|тысяч|млн|миллион|руб|₽)?'
        range_match = re.search(range_pattern, query)
        if range_match:
            min_val = float(range_match.group(1))
            max_val = float(range_match.group(2))
            
            # Определяем единицы измерения
            if "млн" in query or "миллион" in query:
                min_val *= 1000000
                max_val *= 1000000
            elif "тыс" in query or "тысяч" in query:
                min_val *= 1000
                max_val *= 1000
            
            price_range["min"] = min_val
            price_range["max"] = max_val
        
        return price_range if (price_range["min"] is not None or price_range["max"] is not None) else None
    
    def _extract_methods(self, query: str) -> Dict[str, Any]:
        """Извлекает методы закупки из запроса"""
        detected_methods = []
        
        for method_enum, aliases in self.methods_dict.items():
            for alias in aliases:
                if alias.lower() in query:
                    detected_methods.append(method_enum)
                    break
        
        return {"methods": detected_methods}
    
    def _extract_statuses(self, query: str) -> Dict[str, Any]:
        """Извлекает статусы из запроса"""
        detected_statuses = []
        
        for status_enum, aliases in self.statuses_dict.items():
            for alias in aliases:
                if alias.lower() in query:
                    detected_statuses.append(status_enum)
                    break
        
        return {"statuses": detected_statuses}
    
    def _extract_date_range(self, query: str) -> Optional[Dict[str, Any]]:
        """Извлекает временные рамки из запроса"""
        date_rules = []
        result = {
            "publish_from": None,
            "publish_to": None,
            "deadline_from": None,
            "deadline_to": None,
            "rules": []
        }
        
        current_date = datetime.now()
        
        # Относительные периоды для публикации
        if "за неделю" in query or "неделю" in query:
            result["publish_from"] = current_date - timedelta(days=7)
            date_rules.append("new_last_7_days_default")
        elif "за месяц" in query or "месяц" in query:
            result["publish_from"] = current_date - timedelta(days=30)
            date_rules.append("new_last_30_days_default")
        elif "за год" in query:
            result["publish_from"] = current_date - timedelta(days=365)
            date_rules.append("new_last_365_days_default")
        
        # Ключевые слова статусов
        if "новые" in query:
            result["publish_from"] = current_date - timedelta(days=7)
            date_rules.append("new_last_7_days_default")
        
        # Дедлайны
        if "на следующей неделе" in query:
            # Находим следующий понедельник
            days_ahead = 7 - current_date.weekday()
            if days_ahead <= 0:  # Если сегодня понедельник
                days_ahead += 7
            next_monday = current_date + timedelta(days=days_ahead)
            next_sunday = next_monday + timedelta(days=6)
            
            result["deadline_from"] = next_monday
            result["deadline_to"] = next_sunday
            date_rules.append("deadline_next_week")
        
        # Через N дней
        deadline_match = re.search(r'через\s+(\d+)\s+дн', query)
        if deadline_match:
            days = int(deadline_match.group(1))
            result["deadline_from"] = current_date + timedelta(days=days)
            result["deadline_to"] = result["deadline_from"]
            date_rules.append(f"deadline_in_{days}_days")
        
        result["rules"] = date_rules
        return result if any([result["publish_from"], result["publish_to"], result["deadline_from"], result["deadline_to"]]) else None
