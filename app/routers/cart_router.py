from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.data.base import get_db
from app.data.user import User
from app.dto.cart_schemas import (
    CartItemAddRequest,
    CartItemUpdateRequest,
    CartResponse,
)
from app.controllers.cart_controller import CartController
from app.middleware.auth import get_current_user_optional, get_session_id

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    session_id: Optional[str] = Depends(get_session_id),
):
    """Получить текущую корзину (для авторизованного пользователя или гостя)."""
    return CartController.get_cart(db, current_user, session_id)


@router.post("/items", response_model=CartResponse, status_code=201)
def add_item(
    payload: CartItemAddRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    session_id: Optional[str] = Depends(get_session_id),
):
    """Добавить товар в корзину."""
    return CartController.add_item(payload, db, current_user, session_id)


@router.patch("/items/{product_id}", response_model=CartResponse)
def update_item(
    product_id: int,
    payload: CartItemUpdateRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    session_id: Optional[str] = Depends(get_session_id),
):
    """Изменить количество товара в корзине."""
    return CartController.update_item(product_id, payload, db, current_user, session_id)


@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    session_id: Optional[str] = Depends(get_session_id),
):
    """Удалить товар из корзины."""
    return CartController.remove_item(product_id, db, current_user, session_id)


@router.delete("", response_model=CartResponse)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    session_id: Optional[str] = Depends(get_session_id),
):
    """Очистить всю корзину."""
    return CartController.clear_cart(db, current_user, session_id)


@router.post("/merge", response_model=CartResponse)
def merge_guest_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional),
    session_id: Optional[str] = Depends(get_session_id),
):
    """
    Перенести гостевую корзину на авторизованного пользователя.
    Вызывать сразу после логина, передав X-Session-Id и Bearer-токен.
    """
    from fastapi import HTTPException, status
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация")
    if not session_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="X-Session-Id не передан")
    return CartController.merge_guest_cart(session_id, current_user, db)
