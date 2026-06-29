from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.data.base import get_db
from app.data.user import User
from app.dto.brand_schemas import BrandCreateRequest, BrandUpdateRequest, BrandResponse
from app.controllers.brand_controller import BrandController
from app.middleware.auth import require_admin

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.get("/", response_model=List[BrandResponse])
def list_brands(db: Session = Depends(get_db)):

    return BrandController.list_all(db)

@router.get("/{slug}", response_model=BrandResponse)
def get_brand(slug: str, db: Session = Depends(get_db)):
    return BrandController.get_by_slug(slug, db)

@router.post("/", response_model=BrandResponse, status_code=201)
def create_brand(
    payload: BrandCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return BrandController.create(payload, db)

@router.patch("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    payload: BrandUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return BrandController.update(brand_id, payload, db)

@router.delete("/{brand_id}")
def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return BrandController.delete(brand_id, db)
