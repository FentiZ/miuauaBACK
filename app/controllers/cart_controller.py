from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.data.cart import CartItem
from app.data.product import Product
from app.data.user import User
from app.dto.cart_schemas import (
    CartItemAddRequest,
    CartItemUpdateRequest,
    CartItemResponse,
    CartResponse,
)


def _get_cart_items(
    db: Session,
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
) -> list[CartItem]:
    """Возвращает позиции корзины по user_id или session_id."""
    if user_id:
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()
    if session_id:
        return db.query(CartItem).filter(CartItem.session_id == session_id).all()
    return []


def _build_response(items: list[CartItem]) -> CartResponse:
    result: list[CartItemResponse] = []
    for item in items:
        p: Product = item.product
        result.append(
            CartItemResponse(
                product_id=p.id,
                name=p.name,
                slug=p.slug,
                main_image=p.main_image,
                price=p.price,
                quantity=item.quantity,
                stock=p.stock,
                subtotal=round(p.price * item.quantity, 2),
            )
        )
    total_items = sum(i.quantity for i in items)
    total_amount = round(sum(i.product.price * i.quantity for i in items), 2)
    return CartResponse(items=result, total_items=total_items, total_amount=total_amount)


class CartController:

    # ── GET ──────────────────────────────────────────────────────────────────

    @staticmethod
    def get_cart(
        db: Session,
        current_user: Optional[User] = None,
        session_id: Optional[str] = None,
    ) -> CartResponse:
        items = _get_cart_items(
            db,
            user_id=current_user.id if current_user else None,
            session_id=session_id,
        )
        return _build_response(items)

    # ── ADD ──────────────────────────────────────────────────────────────────

    @staticmethod
    def add_item(
        payload: CartItemAddRequest,
        db: Session,
        current_user: Optional[User] = None,
        session_id: Optional[str] = None,
    ) -> CartResponse:
        if not current_user and not session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Необходим токен авторизации или X-Session-Id заголовок",
            )

        product = db.query(Product).filter(
            Product.id == payload.product_id, Product.is_active == True
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден")
        if product.stock < payload.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара на складе (доступно: {product.stock})",
            )

        # Ищем существующую позицию
        query = db.query(CartItem).filter(CartItem.product_id == payload.product_id)
        if current_user:
            query = query.filter(CartItem.user_id == current_user.id)
        else:
            query = query.filter(CartItem.session_id == session_id)
        existing = query.first()

        if existing:
            new_qty = existing.quantity + payload.quantity
            if product.stock < new_qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Недостаточно товара (в корзине уже {existing.quantity}, доступно {product.stock})",
                )
            existing.quantity = new_qty
        else:
            item = CartItem(
                product_id=payload.product_id,
                quantity=payload.quantity,
                user_id=current_user.id if current_user else None,
                session_id=session_id if not current_user else None,
            )
            db.add(item)

        db.commit()
        return CartController.get_cart(db, current_user, session_id)

    # ── UPDATE ───────────────────────────────────────────────────────────────

    @staticmethod
    def update_item(
        product_id: int,
        payload: CartItemUpdateRequest,
        db: Session,
        current_user: Optional[User] = None,
        session_id: Optional[str] = None,
    ) -> CartResponse:
        query = db.query(CartItem).filter(CartItem.product_id == product_id)
        if current_user:
            query = query.filter(CartItem.user_id == current_user.id)
        else:
            query = query.filter(CartItem.session_id == session_id)
        item = query.first()

        if not item:
            raise HTTPException(status_code=404, detail="Позиция не найдена в корзине")

        product = item.product
        if product.stock < payload.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточно товара на складе (доступно: {product.stock})",
            )

        item.quantity = payload.quantity
        db.commit()
        return CartController.get_cart(db, current_user, session_id)

    # ── REMOVE ───────────────────────────────────────────────────────────────

    @staticmethod
    def remove_item(
        product_id: int,
        db: Session,
        current_user: Optional[User] = None,
        session_id: Optional[str] = None,
    ) -> CartResponse:
        query = db.query(CartItem).filter(CartItem.product_id == product_id)
        if current_user:
            query = query.filter(CartItem.user_id == current_user.id)
        else:
            query = query.filter(CartItem.session_id == session_id)
        item = query.first()

        if not item:
            raise HTTPException(status_code=404, detail="Позиция не найдена в корзине")

        db.delete(item)
        db.commit()
        return CartController.get_cart(db, current_user, session_id)

    # ── CLEAR ────────────────────────────────────────────────────────────────

    @staticmethod
    def clear_cart(
        db: Session,
        current_user: Optional[User] = None,
        session_id: Optional[str] = None,
    ) -> CartResponse:
        items = _get_cart_items(
            db,
            user_id=current_user.id if current_user else None,
            session_id=session_id,
        )
        for item in items:
            db.delete(item)
        db.commit()
        return CartResponse(items=[], total_items=0, total_amount=0.0)

    # ── MERGE (guest → user after login) ────────────────────────────────────

    @staticmethod
    def merge_guest_cart(
        session_id: str,
        user: User,
        db: Session,
    ) -> CartResponse:
        """Переносит корзину гостя на авторизованного пользователя."""
        guest_items = db.query(CartItem).filter(CartItem.session_id == session_id).all()

        for guest_item in guest_items:
            existing = db.query(CartItem).filter(
                CartItem.user_id == user.id,
                CartItem.product_id == guest_item.product_id,
            ).first()
            if existing:
                product = guest_item.product
                new_qty = min(existing.quantity + guest_item.quantity, product.stock)
                existing.quantity = new_qty
                db.delete(guest_item)
            else:
                guest_item.user_id = user.id
                guest_item.session_id = None

        db.commit()
        return CartController.get_cart(db, user)
