from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn

from services.search import SearchService
from parser.ru_nlq import NLQParser

app = FastAPI(
    title="UniversalProcureSearch",
    description="Универсальный поиск закупок по сайту zakupki.gov.ru",
    version="1.0.0"
)

# Инициализация сервисов
search_service = SearchService()
nlq_parser = NLQParser()

class SearchRequest(BaseModel):
    q: str
    limit: Optional[int] = 20

class Document(BaseModel):
    title: str
    url: str

class PurchaseItem(BaseModel):
    id: str
    title: str
    description: str
    customer: str
    region: str
    okpd2: List[str]
    price: float
    currency: str = "RUB"
    method: str
    status: str
    publish_dt: datetime
    bid_deadline_dt: Optional[datetime] = None
    url: str
    documents: List[Document] = []

class Diagnostics(BaseModel):
    matched_keywords: List[str]
    matched_okpd2: List[str]
    regions_detected: List[str]
    method_detected: Optional[str] = None
    status_detected: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    date_rules: List[str]

class SearchResponse(BaseModel):
    filters: Dict[str, Any]
    items: List[PurchaseItem]
    total: int
    query_time_ms: float
    diagnostics: Diagnostics

@app.get("/")
async def root():
    return {"message": "UniversalProcureSearch API", "version": "1.0.0"}

@app.post("/search", response_model=SearchResponse)
async def search_purchases(request: SearchRequest):
    """
    Поиск закупок по естественному языковому запросу
    """
    try:
        import time
        start_time = time.time()
        
        # Парсим естественный язык в фильтры
        filters = nlq_parser.parse(request.q)
        
        # Извлекаем диагностику
        diagnostics_data = filters.pop("diagnostics", {})
        
        # Выполняем поиск
        results = await search_service.search(filters, request.limit)
        
        query_time = (time.time() - start_time) * 1000
        
        # Создаем объект диагностики
        diagnostics = Diagnostics(
            matched_keywords=diagnostics_data.get("matched_keywords", []),
            matched_okpd2=diagnostics_data.get("matched_okpd2", []),
            regions_detected=diagnostics_data.get("regions_detected", []),
            method_detected=diagnostics_data.get("method_detected"),
            status_detected=diagnostics_data.get("status_detected"),
            price_min=diagnostics_data.get("price_min"),
            price_max=diagnostics_data.get("price_max"),
            date_rules=diagnostics_data.get("date_rules", [])
        )
        
        return SearchResponse(
            filters=filters,
            items=results,
            total=len(results),
            query_time_ms=round(query_time, 2),
            diagnostics=diagnostics
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка поиска: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
