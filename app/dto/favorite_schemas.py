from pydantic import BaseModel
from typing import List
from app.dto.product_schemas import ProductCardResponse

class FavoriteResponse(BaseModel):
    items: List[ProductCardResponse]
    total: int
