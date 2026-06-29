from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.data.base import Base


class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    # email и phone — оба опциональны, но хотя бы одно должно быть заполнено
    # (контролируется на уровне схемы/контроллера)
    email    = Column(String(255), unique=True, index=True, nullable=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    phone    = Column(String(32),  unique=True, index=True, nullable=True)
    full_name       = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role        = Column(SAEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active   = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    addresses     = relationship("Address",     back_populates="user", cascade="all, delete-orphan")
    cart_items    = relationship("CartItem",    back_populates="user", cascade="all, delete-orphan")
    favorites     = relationship("FavoriteItem",back_populates="user", cascade="all, delete-orphan")
    compare_items = relationship("CompareItem", back_populates="user", cascade="all, delete-orphan")
    orders        = relationship("Order",       back_populates="user")
    reviews       = relationship("Review",      back_populates="user", cascade="all, delete-orphan")

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def __repr__(self) -> str:
        identifier = self.email or self.phone or self.username
        return f"<User id={self.id} login={identifier}>"
