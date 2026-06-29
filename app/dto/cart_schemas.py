from pydantic import BaseModel, field_validator
from typing import Optional, List

class CartItemAddRequest(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Количество должно быть не меньше 1")
        return v

class CartItemUpdateRequest(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Количество должно быть не меньше 1")
        return v

class CartItemResponse(BaseModel):
    product_id: int
    name: str
    slug: str
    main_image: Optional[str] = None
    price: float
    quantity: int
    stock: int
    subtotal: float

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_items: int
    total_amount: float
