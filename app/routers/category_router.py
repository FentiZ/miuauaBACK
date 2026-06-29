from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.data.base import get_db
from app.data.user import User
from app.dto.category_schemas import (
    CategoryCreateRequest, CategoryUpdateRequest, CategoryResponse, CategoryTreeResponse,
)
from app.controllers.category_controller import CategoryController
from app.middleware.auth import require_admin

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategoryTreeResponse])
def get_category_tree(db: Session = Depends(get_db)):

    return CategoryController.get_tree(db)

@router.get("/flat", response_model=List[CategoryResponse])
def get_categories_flat(db: Session = Depends(get_db)):

    return CategoryController.list_flat(db)

@router.get("/{slug}", response_model=CategoryResponse)
def get_category(slug: str, db: Session = Depends(get_db)):

    return CategoryController.get_by_slug(slug, db)

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    payload: CategoryCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return CategoryController.create(payload, db)

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return CategoryController.update(category_id, payload, db)

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return CategoryController.delete(category_id, db)
