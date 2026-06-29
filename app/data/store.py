from sqlalchemy import Column, Integer, String, Float, Boolean
from app.data.base import Base

class Store(Base):
    __tablename__ = "stores"

    id            = Column(Integer, primary_key=True, index=True)
    city          = Column(String(150), nullable=False, index=True)
    address       = Column(String(500), nullable=False)
    phone         = Column(String(32), nullable=True)
    working_hours = Column(String(150), nullable=True)
    latitude      = Column(Float, nullable=True)
    longitude     = Column(Float, nullable=True)
    is_active     = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Store id={self.id} city={self.city}>"
