from sqlalchemy import Column, Integer, String, Boolean
from app.data.base import Base

class Banner(Base):
    __tablename__ = "banners"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=True)
    image_url  = Column(String(500), nullable=False)
    link_url   = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0)
    is_active  = Column(Boolean, default=True)

    def __repr__(self) -> str:
        return f"<Banner id={self.id} title={self.title}>"
