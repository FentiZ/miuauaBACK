from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.data.base import Base

class ProductImage(Base):
    __tablename__ = "product_images"

    id          = Column(Integer, primary_key=True, index=True)
    product_id  = Column(Integer, ForeignKey("products.id"), nullable=False)

    image_url   = Column(String(500), nullable=False)
    color_name  = Column(String(100), nullable=True)
    color_hex   = Column(String(7), nullable=True)
    is_main     = Column(Boolean, default=False)
    sort_order  = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")

    def __repr__(self) -> str:
        return f"<ProductImage id={self.id} product_id={self.product_id}>"
