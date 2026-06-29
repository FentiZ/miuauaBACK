from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ProductImageCreateRequest(BaseModel):
    image_url: str
    color_name: Optional[str] = None
    color_hex: Optional[str] = None
    is_main: bool = False
    sort_order: int = 0

class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    color_name: Optional[str]
    color_hex: Optional[str]
    is_main: bool
    sort_order: int

    model_config = {"from_attributes": True}

class ProductSpecificationCreateRequest(BaseModel):
    group_name: str
    name: str
    value: str
    sort_order: int = 0

class ProductSpecificationResponse(BaseModel):
    id: int
    group_name: str
    name: str
    value: str
    sort_order: int

    model_config = {"from_attributes": True}

class ProductCreateRequest(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: float
    old_price: Optional[float] = None
    category_id: int
    brand_id: Optional[int] = None
    sku: Optional[str] = None
    stock: int = 0
    is_new: bool = False
    is_top: bool = False
    loyalty_partner: Optional[str] = None
    review_bonus_points: Optional[int] = None
    images: List[ProductImageCreateRequest] = []
    specifications: List[ProductSpecificationCreateRequest] = []

    @field_validator("price")
    @classmethod
    def price_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError("Цена не может быть отрицательной")
        return round(v, 2)

    @field_validator("old_price")
    @classmethod
    def old_price_non_negative(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v < 0:
            raise ValueError("Старая цена не может быть отрицательной")
        return round(v, 2) if v is not None else v

    @field_validator("stock")
    @classmethod
    def stock_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Количество не может быть отрицательным")
        return v

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[float] = None
    old_price: Optional[float] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    sku: Optional[str] = None
    stock: Optional[int] = None
    is_new: Optional[bool] = None
    is_top: Optional[bool] = None
    is_active: Optional[bool] = None
    loyalty_partner: Optional[str] = None
    review_bonus_points: Optional[int] = None

class BrandShortResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}

class CategoryShortResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}

class ProductCardResponse(BaseModel):

    id: int
    name: str
    slug: str
    price: float
    old_price: Optional[float]
    discount_percent: int
    main_image: Optional[str] = None
    rating_avg: float
    reviews_count: int
    has_reviews: bool
    stock: int
    is_new: bool
    is_top: bool
    loyalty_partner: Optional[str] = None
    review_bonus_points: Optional[int] = None
    brand: Optional[BrandShortResponse] = None

    model_config = {"from_attributes": True}

class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    short_description: Optional[str]
    price: float
    old_price: Optional[float]
    discount_percent: int
    sku: Optional[str]
    stock: int
    rating_avg: float
    reviews_count: int
    view_count: int
    is_new: bool
    is_top: bool
    is_active: bool
    category: Optional[CategoryShortResponse] = None
    brand: Optional[BrandShortResponse] = None
    images: List[ProductImageResponse] = []
    specifications: List[ProductSpecificationResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProductListResponse(BaseModel):
    items: List[ProductCardResponse]
    total: int
    page: int
    page_size: int
    pages: int

class ProductSortOption(str, Enum):
    POPULAR = "popular"
    NEW = "new"
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    RATING = "rating"
    DISCOUNT = "discount"

class ProductSearchParams(BaseModel):
    query: Optional[str] = None
    category_id: Optional[int] = None
    category_slug: Optional[str] = None
    brand_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None
    is_new: Optional[bool] = None
    is_top: Optional[bool] = None
    discounted: Optional[bool] = None
    sort: ProductSortOption = ProductSortOption.POPULAR
    page: int = 1
    page_size: int = 20

    @field_validator("page")
    @classmethod
    def page_positive(cls, v: int) -> int:
        return max(1, v)

    @field_validator("page_size")
    @classmethod
    def page_size_limit(cls, v: int) -> int:
        return min(max(1, v), 100)
