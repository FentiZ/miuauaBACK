from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.data.base import Base

class FavoriteItem(Base):
    __tablename__ = "favorite_items"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_favorite_user_product"),
    )

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user    = relationship("User", back_populates="favorites")
    product = relationship("Product")

    def __repr__(self) -> str:
        return f"<FavoriteItem user_id={self.user_id} product_id={self.product_id}>"
