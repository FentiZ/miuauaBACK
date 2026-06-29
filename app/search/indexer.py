from typing import Optional
from datetime import datetime

from app.data.product import Product
from app.search.client import get_es_client, ensure_index

def _product_to_doc(product: Product) -> dict:
    return {
        "id":                  product.id,
        "name":                product.name,
        "slug":                product.slug,
        "description":         product.description or "",
        "short_description":   product.short_description or "",
        "price":               product.price,
        "old_price":           product.old_price,
        "sku":                 product.sku,
        "stock":               product.stock,
        "category_id":         product.category_id,
        "category_name":       product.category.name if product.category else None,
        "category_slug":       product.category.slug if product.category else None,
        "brand_id":            product.brand_id,
        "brand_name":          product.brand.name if product.brand else None,
        "brand_slug":          product.brand.slug if product.brand else None,
        "rating_avg":          product.rating_avg,
        "reviews_count":       product.reviews_count,
        "view_count":          product.view_count,
        "is_new":              product.is_new,
        "is_top":              product.is_top,
        "is_active":           product.is_active,
        "discount_percent":    product.discount_percent,
        "loyalty_partner":     product.loyalty_partner,
        "review_bonus_points": product.review_bonus_points,
        "main_image":          product.main_image,
        "created_at":          product.created_at.isoformat() if product.created_at else None,
        "updated_at":          product.updated_at.isoformat() if product.updated_at else None,
    }

def index_product(product: Product, index: str) -> bool:
    client = get_es_client()
    if client is None:
        return False
    ensure_index(index)
    try:
        client.index(index=index, id=product.id, document=_product_to_doc(product))
        return True
    except Exception:
        return False

def index_product_all(product: Product, indices: dict) -> None:
    for index in indices.values():
        index_product(product, index)

def delete_product(product_id: int, index: str) -> bool:
    client = get_es_client()
    if client is None:
        return False
    try:
        client.delete(index=index, id=product_id, ignore=[404])
        return True
    except Exception:
        return False

def delete_product_all(product_id: int, indices: dict) -> None:
    for index in indices.values():
        delete_product(product_id, index)

def reindex_all(products: list, index: str) -> int:
    client = get_es_client()
    if client is None:
        return 0
    ensure_index(index)
    count = 0
    for product in products:
        try:
            client.index(index=index, id=product.id, document=_product_to_doc(product))
            count += 1
        except Exception:
            pass
    return count
