from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.data.base import Base

class OrderStatus(str, enum.Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class DeliveryMethod(str, enum.Enum):
    COURIER = "courier"
    NOVA_POSHTA = "nova_poshta"
    PICKUP = "pickup"

class PaymentMethod(str, enum.Enum):
    CARD_ONLINE = "card_online"
    CASH_ON_DELIVERY = "cash_on_delivery"
    CARD_ON_DELIVERY = "card_on_delivery"

class Order(Base):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(32), unique=True, index=True, nullable=False)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=True)

    full_name = Column(String(255), nullable=False)
    phone     = Column(String(32), nullable=False)
    email     = Column(String(255), nullable=True)

    city             = Column(String(150), nullable=False)
    delivery_method  = Column(SAEnum(DeliveryMethod), nullable=False)
    delivery_address = Column(Text, nullable=True)
    store_id         = Column(Integer, ForeignKey("stores.id"), nullable=True)

    payment_method = Column(SAEnum(PaymentMethod), nullable=False)
    comment        = Column(Text, nullable=True)

    status       = Column(SAEnum(OrderStatus), default=OrderStatus.NEW, nullable=False)
    total_amount = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user  = relationship("User", back_populates="orders")
    store = relationship("Store")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Order id={self.id} number={self.order_number} status={self.status}>"

class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    product_name  = Column(String(255), nullable=False)
    product_image = Column(String(500), nullable=True)
    price         = Column(Float, nullable=False)
    quantity      = Column(Integer, nullable=False)

    order   = relationship("Order", back_populates="items")
    product = relationship("Product")

    @property
    def subtotal(self) -> float:
        return round(self.price * self.quantity, 2)

    def __repr__(self) -> str:
        return f"<OrderItem order_id={self.order_id} product={self.product_name} qty={self.quantity}>"
