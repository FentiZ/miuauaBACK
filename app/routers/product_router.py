from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.data.base import get_db
from app.data.user import User
from app.dto.product_schemas import (
    ProductCreateRequest, ProductUpdateRequest, ProductImageCreateRequest,
    ProductSpecificationCreateRequest,
    ProductResponse, ProductCardResponse, ProductListResponse,
    ProductSearchParams, ProductSortOption,
)
from app.controllers.product_controller import ProductController
from app.middleware.auth import require_admin

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/search", response_model=ProductListResponse)
def search_products(
    query: Optional[str] = Query(None, description="Текстовый поиск по названию/описанию"),
    category_id: Optional[int] = Query(None),
    category_slug: Optional[str] = Query(None, description="Например: televizory"),
    brand_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: Optional[bool] = Query(None),
    is_new: Optional[bool] = Query(None, description="Только секция «Новинки»"),
    is_top: Optional[bool] = Query(None, description="Только секция «Лидеры продаж»"),
    discounted: Optional[bool] = Query(None, description="Только товары со скидкой (раздел «Акции»)"),
    sort: ProductSortOption = Query(ProductSortOption.POPULAR),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):

    params = ProductSearchParams(
        query=query, category_id=category_id, category_slug=category_slug, brand_id=brand_id,
        min_price=min_price, max_price=max_price, in_stock=in_stock,
        is_new=is_new, is_top=is_top, discounted=discounted,
        sort=sort, page=page, page_size=page_size,
    )
    return ProductController.search(params, db)

@router.get("/{id_or_slug}", response_model=ProductResponse)
def get_product(id_or_slug: str, db: Session = Depends(get_db)):

    return ProductController.get_by_id_or_slug(id_or_slug, db)

@router.get("/{product_id}/related", response_model=List[ProductCardResponse])
def get_related_products(product_id: int, limit: int = Query(8, ge=1, le=20), db: Session = Depends(get_db)):

    return ProductController.related(product_id, db, limit)

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    payload: ProductCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return ProductController.create(payload, admin, db)

@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    payload: ProductUpdateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return ProductController.update(product_id, payload, admin, db)

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return ProductController.delete(product_id, admin, db)

@router.post("/{product_id}/images", response_model=ProductResponse, status_code=201)
def add_product_image(
    product_id: int,
    payload: ProductImageCreateRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return ProductController.add_image(product_id, payload, admin, db)

@router.delete("/{product_id}/images/{image_id}")
def delete_product_image(
    product_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return ProductController.delete_image(product_id, image_id, admin, db)

@router.put("/{product_id}/specifications", response_model=ProductResponse)
def set_product_specifications(
    product_id: int,
    specs: List[ProductSpecificationCreateRequest],
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):

    return ProductController.set_specifications(product_id, specs, admin, db)
