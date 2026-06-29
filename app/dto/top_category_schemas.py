from pydantic import BaseModel
from typing import Optional, List


class TopCategoryCreateRequest(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int = 0
    is_top: bool = False
    category_id: Optional[int] = None


class TopCategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    is_top: Optional[bool] = None
    category_id: Optional[int] = None


class TopCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    image_url: Optional[str]
    sort_order: int
    is_active: bool
    is_top: bool
    category_id: Optional[int]

    model_config = {"from_attributes": True}


class TopCategoryWithDownResponse(TopCategoryResponse):
    """TopCategory с вложенной лентой DownCategory."""
    down_categories: List["DownCategoryResponse"] = []


# Импорт ниже, чтобы избежать циклического импорта
from app.dto.down_category_schemas import DownCategoryResponse  # noqa: E402

TopCategoryWithDownResponse.model_rebuild()
