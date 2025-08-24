from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.purchase import Purchase, Document, Favorite
from app.schemas.purchase import (
    PurchaseCreate, 
    PurchaseUpdate, 
    PurchaseResponse,
    PurchaseListResponse,
    SearchFilters
)
from app.core.auth import get_current_user
from app.services.purchase_service import PurchaseService

router = APIRouter()

@router.get("/", response_model=PurchaseListResponse)
async def get_purchases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получить список закупок с пагинацией"""
    service = PurchaseService(db)
    purchases, total = service.get_purchases(skip=skip, limit=limit)
    
    return PurchaseListResponse(
        items=purchases,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/search", response_model=PurchaseListResponse)
async def search_purchases(
    query: Optional[str] = Query(None, description="Поисковый запрос"),
    region: Optional[str] = Query(None, description="Регион"),
    price_min: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    price_max: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    status: Optional[str] = Query(None, description="Статус закупки"),
    procurement_method: Optional[str] = Query(None, description="Способ закупки"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Поиск закупок по фильтрам"""
    filters = SearchFilters(
        query=query,
        region=region,
        price_min=price_min,
        price_max=price_max,
        status=status,
        procurement_method=procurement_method
    )
    
    service = PurchaseService(db)
    purchases, total = service.search_purchases(filters, skip=skip, limit=limit)
    
    return PurchaseListResponse(
        items=purchases,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/{purchase_id}", response_model=PurchaseResponse)
async def get_purchase(
    purchase_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получить детальную информацию о закупке"""
    service = PurchaseService(db)
    purchase = service.get_purchase_by_id(purchase_id)
    
    if not purchase:
        raise HTTPException(status_code=404, detail="Закупка не найдена")
    
    return purchase

@router.post("/{purchase_id}/favorite")
async def toggle_favorite(
    purchase_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Добавить/убрать закупку из избранного"""
    service = PurchaseService(db)
    is_favorite = service.toggle_favorite(purchase_id, current_user)
    
    return {
        "purchase_id": purchase_id,
        "is_favorite": is_favorite,
        "message": "Добавлено в избранное" if is_favorite else "Убрано из избранного"
    }

@router.get("/favorites/list", response_model=PurchaseListResponse)
async def get_favorites(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получить избранные закупки пользователя"""
    service = PurchaseService(db)
    purchases, total = service.get_user_favorites(current_user, skip=skip, limit=limit)
    
    return PurchaseListResponse(
        items=purchases,
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/regions/list")
async def get_regions(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получить список доступных регионов"""
    service = PurchaseService(db)
    regions = service.get_regions()
    
    return {"regions": regions}

@router.get("/statuses/list")
async def get_statuses(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получить список доступных статусов"""
    return {
        "statuses": [
            {"value": "draft", "label": "Черновик"},
            {"value": "published", "label": "Опубликовано"},
            {"value": "bidding", "label": "Подача заявок"},
            {"value": "evaluation", "label": "Рассмотрение"},
            {"value": "awarded", "label": "Присуждено"},
            {"value": "completed", "label": "Завершено"},
            {"value": "cancelled", "label": "Отменено"},
        ]
    }

@router.get("/methods/list")
async def get_procurement_methods(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """Получить список способов закупки"""
    return {
        "methods": [
            {"value": "electronic_auction", "label": "Электронный аукцион"},
            {"value": "tender", "label": "Открытый конкурс"},
            {"value": "request_quotes", "label": "Запрос котировок"},
            {"value": "request_proposals", "label": "Запрос предложений"},
            {"value": "limited_competition", "label": "Конкурс с ограниченным участием"},
        ]
    }
