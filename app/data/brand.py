from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship

from app.data.base import Base

class Brand(Base):
    __tablename__ = "brands"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(150), unique=True, nullable=False)
    slug        = Column(String(150), unique=True, index=True, nullable=False)
    logo_url    = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    is_active   = Column(Boolean, default=True)

    products = relationship("Product", back_populates="brand")

    def __repr__(self) -> str:
        return f"<Brand id={self.id} name={self.name}>"
