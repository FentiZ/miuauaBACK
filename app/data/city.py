from sqlalchemy import Column, Integer, String
from app.data.base import Base

class City(Base):
    __tablename__ = "cities"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    slug = Column(String(150), unique=True, index=True, nullable=False)

    def __repr__(self) -> str:
        return f"<City id={self.id} name={self.name}>"
