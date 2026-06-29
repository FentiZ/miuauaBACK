from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.data.base import Base

class Address(Base):
    __tablename__ = "addresses"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)

    full_name   = Column(String(255), nullable=False)
    phone       = Column(String(32), nullable=False)
    city        = Column(String(150), nullable=False, index=True)
    region      = Column(String(150), nullable=True)
    street      = Column(String(255), nullable=False)
    house       = Column(String(50), nullable=False)
    apartment   = Column(String(50), nullable=True)
    postal_code = Column(String(20), nullable=True)
    is_default  = Column(Boolean, default=False)

    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"<Address id={self.id} city={self.city} street={self.street}>"
