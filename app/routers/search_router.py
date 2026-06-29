import math
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.data.base import get_db
from app.data.product import Product
from app.data.user import User
from app.dto.product_schemas import ProductListResponse, ProductCardResponse, ProductSearchParams, ProductSortOption
from app.middleware.auth import require_admin
from app.search.config import ES_INDICES, ES_DEFAULT_INDEX
from app.search.service import search_products, search_across_indices, suggest_products
from app.search.indexer import index_product_all, reindex_all, delete_product_all
from app.search.client import ensure_all_indices
from app.controllers.product_controller import ProductController

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/products", response_model=ProductListResponse)
def search(
    query: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    category_slug: Optional[str] = Query(None),
    brand_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: Optional[bool] = Query(None),
    is_new: Optional[bool] = Query(None),
    is_top: Optional[bool] = Query(None),
    discounted: Optional[bool] = Query(None),
    sort: ProductSortOption = Query(ProductSortOption.POPULAR),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    index: Optional[str] = Query(None, description="ES index name. Available: " + ", ".join(ES_INDICES.keys())),
    db: Session = Depends(get_db),
):
    params = ProductSearchParams(
        query=query, category_id=category_id, category_slug=category_slug,
        brand_id=brand_id, min_price=min_price, max_price=max_price,
        in_stock=in_stock, is_new=is_new, is_top=is_top, discounted=discounted,
        sort=sort, page=page, page_size=page_size,
    )

    target_index = ES_INDICES.get(index, ES_DEFAULT_INDEX) if index else None
    result = search_products(params, target_index)

    if result is None:
        return ProductController.search(params, db)

    items_data = result["items"]
    total = result["total"]
    pages = math.ceil(total / page_size) if total > 0 else 1

    ids = [item["id"] for item in items_data]
    products = db.query(Product).filter(Product.id.in_(ids)).all()
    product_map = {p.id: p for p in products}
    ordered = [product_map[i] for i in ids if i in product_map]

    return ProductListResponse(
        items=[ProductCardResponse.model_validate(p) for p in ordered],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )

@router.get("/products/multi", response_model=ProductListResponse)
def search_multi_index(
    query: Optional[str] = Query(None),
    indices: Optional[str] = Query(None, description="Comma-separated index names, e.g. products_ua,products_ru"),
    category_slug: Optional[str] = Query(None),
    brand_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort: ProductSortOption = Query(ProductSortOption.POPULAR),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    params = ProductSearchParams(
        query=query, category_slug=category_slug, brand_id=brand_id,
        min_price=min_price, max_price=max_price,
        sort=sort, page=page, page_size=page_size,
    )

    index_list = [i.strip() for i in indices.split(",")] if indices else None
    result = search_across_indices(params, index_list)

    if result is None:
        return ProductController.search(params, db)

    items_data = result["items"]
    total = result["total"]
    pages = math.ceil(total / page_size) if total > 0 else 1

    ids = [item["id"] for item in items_data]
    products = db.query(Product).filter(Product.id.in_(ids)).all()
    product_map = {p.id: p for p in products}
    ordered = [product_map[i] for i in ids if i in product_map]

    return ProductListResponse(
        items=[ProductCardResponse.model_validate(p) for p in ordered],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )

@router.get("/suggest", response_model=List[str])
def suggest(
    q: str = Query(..., min_length=1),
    index: Optional[str] = Query(None),
):
    target_index = ES_INDICES.get(index, ES_DEFAULT_INDEX) if index else None
    return suggest_products(q, target_index)

@router.post("/admin/reindex", status_code=200)
def reindex(
    index: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    target_index = ES_INDICES.get(index) if index else None
    products = db.query(Product).filter(Product.is_active == True).all()

    if target_index:
        count = reindex_all(products, target_index)
        return {"indexed": count, "index": target_index}

    results = {}
    for key, idx in ES_INDICES.items():
        results[key] = reindex_all(products, idx)
    return {"indexed": results}

@router.get("/admin/indices", status_code=200)
def list_indices(admin: User = Depends(require_admin)):
    ensure_all_indices(ES_INDICES)
    return {"indices": ES_INDICES, "default": ES_DEFAULT_INDEX}
