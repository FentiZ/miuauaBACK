from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.data.base import get_db
from app.data.user import User
from app.dto.back_category_schemas import (
    BackCategoryCreateRequest,
    BackCategoryUpdateRequest,
    BackCategoryResponse,
    BackCategoryTreeResponse,
)
from app.controllers.back_category_controller import BackCategoryController
from app.middleware.auth import require_admin

router = APIRouter(prefix="/back-categories", tags=["BackCategories"])


@router.get("/", response_model=List[BackCategoryTreeResponse])
def get_back_category_tree(db: Session = Depends(get_db)):
    """Дерево бокового меню (с вложенными дочерними пунктами)."""
    return BackCategoryController.get_tree(db)


@router.get("/flat", response_model=List[BackCategoryResponse])
def list_back_categories_flat(db: Session = Depends(get_db)):
    """Плоский список всех BackCategory."""
    return BackCategoryController.list_flat(db)


@router.get("/{slug}", response_model=BackCategoryResponse)
def get_back_category(slug: str, db: Session = Depends(get_db)):
    return BackCategoryController.get_by_slug(slug, db)


@router.post("/", response_model=BackCategoryResponse, status_code=201)
def create_back_category(
    payload: BackCategoryCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return BackCategoryController.create(payload, db)


@router.patch("/{item_id}", response_model=BackCategoryResponse)
def update_back_category(
    item_id: int,
    payload: BackCategoryUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return BackCategoryController.update(item_id, payload, db)


@router.delete("/{item_id}")
def delete_back_category(
    item_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return BackCategoryController.delete(item_id, db)
