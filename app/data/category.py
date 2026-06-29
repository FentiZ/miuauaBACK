from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.data.base import Base

class Category(Base):
    __tablename__ = "categories"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255), nullable=False)
    slug        = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url   = Column(String(500), nullable=True)
    parent_id   = Column(Integer, ForeignKey("categories.id"), nullable=True)
    sort_order  = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)

    parent   = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name}>"
