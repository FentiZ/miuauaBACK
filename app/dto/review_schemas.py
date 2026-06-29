from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class ReviewCreateRequest(BaseModel):
    rating: int
    pros: Optional[str] = None
    cons: Optional[str] = None
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: int) -> int:
        if v < 1 or v > 5:
            raise ValueError("Рейтинг должен быть от 1 до 5")
        return v

class ReviewUserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str] = None

    model_config = {"from_attributes": True}

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    rating: int
    pros: Optional[str]
    cons: Optional[str]
    comment: Optional[str]
    created_at: datetime
    user: ReviewUserResponse

    model_config = {"from_attributes": True}

class ReviewListResponse(BaseModel):
    items: list[ReviewResponse]
    total: int
    page: int
    page_size: int
    pages: int
    rating_avg: float
