from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from app.data.base import Base

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("product_id", "user_id", name="uq_review_product_user"),
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range"),
    )

    id         = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)

    rating     = Column(Integer, nullable=False)
    pros       = Column(Text, nullable=True)
    cons       = Column(Text, nullable=True)
    comment    = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")
    user    = relationship("User", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review id={self.id} product_id={self.product_id} rating={self.rating}>"
