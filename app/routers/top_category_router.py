from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.data.base import get_db
from app.data.user import User
from app.dto.top_category_schemas import (
    TopCategoryCreateRequest,
    TopCategoryUpdateRequest,
    TopCategoryResponse,
    TopCategoryWithDownResponse,
)
from app.controllers.top_category_controller import TopCategoryController
from app.middleware.auth import require_admin

router = APIRouter(prefix="/top-categories", tags=["TopCategories"])


@router.get("/", response_model=List[TopCategoryResponse])
def list_top_categories(db: Session = Depends(get_db)):
    """Все активные TopCategory, отсортированные по sort_order."""
    return TopCategoryController.list_all(db)


@router.get("/with-down", response_model=List[TopCategoryWithDownResponse])
def list_top_with_down(db: Session = Depends(get_db)):
    """TopCategory с вложенными DownCategory (для рендера всей полосы за один запрос)."""
    return TopCategoryController.list_with_down(db)


@router.get("/{slug}", response_model=TopCategoryResponse)
def get_top_category(slug: str, db: Session = Depends(get_db)):
    return TopCategoryController.get_by_slug(slug, db)


@router.post("/", response_model=TopCategoryResponse, status_code=201)
def create_top_category(
    payload: TopCategoryCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return TopCategoryController.create(payload, db)


@router.patch("/{item_id}", response_model=TopCategoryResponse)
def update_top_category(
    item_id: int,
    payload: TopCategoryUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return TopCategoryController.update(item_id, payload, db)


@router.delete("/{item_id}")
def delete_top_category(
    item_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return TopCategoryController.delete(item_id, db)
