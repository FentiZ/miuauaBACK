from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.data.base import get_db
from app.data.user import User
from app.dto.down_category_schemas import (
    DownCategoryCreateRequest,
    DownCategoryUpdateRequest,
    DownCategoryResponse,
)
from app.controllers.down_category_controller import DownCategoryController
from app.middleware.auth import require_admin

router = APIRouter(prefix="/down-categories", tags=["DownCategories"])


@router.get("/", response_model=List[DownCategoryResponse])
def list_down_categories(
    top_category_id: Optional[int] = Query(None, description="Фильтр по TopCategory"),
    db: Session = Depends(get_db),
):
    """
    Горизонтальная лента категорий.
    Передайте ?top_category_id=<id> чтобы получить ленту для конкретной TopCategory-вкладки.
    """
    return DownCategoryController.list_all(db, top_category_id)


@router.get("/{slug}", response_model=DownCategoryResponse)
def get_down_category(slug: str, db: Session = Depends(get_db)):
    return DownCategoryController.get_by_slug(slug, db)


@router.post("/", response_model=DownCategoryResponse, status_code=201)
def create_down_category(
    payload: DownCategoryCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return DownCategoryController.create(payload, db)


@router.patch("/{item_id}", response_model=DownCategoryResponse)
def update_down_category(
    item_id: int,
    payload: DownCategoryUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return DownCategoryController.update(item_id, payload, db)


@router.delete("/{item_id}")
def delete_down_category(
    item_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return DownCategoryController.delete(item_id, db)
