from typing import Optional, List

from app.search.client import get_es_client
from app.search.config import ES_DEFAULT_INDEX, ES_INDICES
from app.dto.product_schemas import ProductSearchParams, ProductSortOption

def _build_query(params: ProductSearchParams) -> dict:
    must = []
    filters = [{"term": {"is_active": True}}]

    if params.query:
        must.append({
            "multi_match": {
                "query": params.query,
                "fields": ["name^3", "description", "short_description", "brand_name^2", "category_name"],
                "type": "best_fields",
                "fuzziness": "AUTO",
            }
        })

    if params.category_slug:
        filters.append({"term": {"category_slug": params.category_slug}})
    elif params.category_id:
        filters.append({"term": {"category_id": params.category_id}})

    if params.brand_id:
        filters.append({"term": {"brand_id": params.brand_id}})

    if params.min_price is not None or params.max_price is not None:
        price_range: dict = {}
        if params.min_price is not None:
            price_range["gte"] = params.min_price
        if params.max_price is not None:
            price_range["lte"] = params.max_price
        filters.append({"range": {"price": price_range}})

    if params.in_stock is True:
        filters.append({"range": {"stock": {"gt": 0}}})
    elif params.in_stock is False:
        filters.append({"term": {"stock": 0}})

    if params.is_new is True:
        filters.append({"term": {"is_new": True}})
    if params.is_top is True:
        filters.append({"term": {"is_top": True}})
    if params.discounted is True:
        filters.append({"range": {"discount_percent": {"gt": 0}}})

    return {
        "bool": {
            "must": must if must else [{"match_all": {}}],
            "filter": filters,
        }
    }

def _build_sort(sort: ProductSortOption) -> list:
    if sort == ProductSortOption.NEW:
        return [{"created_at": "desc"}]
    if sort == ProductSortOption.PRICE_ASC:
        return [{"price": "asc"}]
    if sort == ProductSortOption.PRICE_DESC:
        return [{"price": "desc"}]
    if sort == ProductSortOption.RATING:
        return [{"rating_avg": "desc"}, {"reviews_count": "desc"}]
    if sort == ProductSortOption.DISCOUNT:
        return [{"discount_percent": "desc"}]
    return [{"view_count": "desc"}, {"rating_avg": "desc"}]

def search_products(
    params: ProductSearchParams,
    index: Optional[str] = None,
) -> Optional[dict]:
    client = get_es_client()
    if client is None:
        return None

    target_index = index or ES_DEFAULT_INDEX
    offset = (params.page - 1) * params.page_size

    body = {
        "query": _build_query(params),
        "sort": _build_sort(params.sort),
        "from": offset,
        "size": params.page_size,
        "_source": True,
    }

    try:
        result = client.search(index=target_index, body=body)
        hits = result["hits"]
        total = hits["total"]["value"]
        items = [h["_source"] for h in hits["hits"]]
        return {"items": items, "total": total}
    except Exception:
        return None

def search_across_indices(
    params: ProductSearchParams,
    indices: Optional[List[str]] = None,
) -> Optional[dict]:
    client = get_es_client()
    if client is None:
        return None

    targets = indices or list(ES_INDICES.values())
    offset = (params.page - 1) * params.page_size

    body = {
        "query": _build_query(params),
        "sort": _build_sort(params.sort),
        "from": offset,
        "size": params.page_size,
        "_source": True,
    }

    try:
        result = client.search(index=",".join(targets), body=body)
        hits = result["hits"]
        total = hits["total"]["value"]
        items = [h["_source"] for h in hits["hits"]]
        return {"items": items, "total": total}
    except Exception:
        return None

def suggest_products(query: str, index: Optional[str] = None, size: int = 5) -> List[str]:
    client = get_es_client()
    if client is None:
        return []

    target_index = index or ES_DEFAULT_INDEX
    body = {
        "suggest": {
            "name_suggest": {
                "prefix": query,
                "completion": {
                    "field": "name",
                    "size": size,
                    "skip_duplicates": True,
                }
            }
        }
    }

    try:
        result = client.search(index=target_index, body=body)
        options = result.get("suggest", {}).get("name_suggest", [])
        if options:
            return [o["text"] for o in options[0].get("options", [])]
        return []
    except Exception:
        return []
