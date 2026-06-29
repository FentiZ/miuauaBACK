from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.data.base import Base


class TopCategory(Base):
    """
    Горизонтальная полоса вкладок над секцией «Лідери продажу» (Скрин 1).

    is_top  — помечает вкладку «ТОП товари» (выделяется цветом/стилем).
    Все остальные вкладки — обычные, is_top=False.
    """
    __tablename__ = "top_categories"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255), nullable=False)
    slug        = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    image_url   = Column(String(500), nullable=True)
    sort_order  = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)

    # Является ли эта вкладка «топ»-вкладкой (ТОП товари).
    # У одной вкладки в наборе должно быть True; остальные — False.
    is_top      = Column(Boolean, default=False, nullable=False)

    # Опциональная ссылка на «настоящую» категорию каталога
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category    = relationship("Category", backref="top_entries")

    def __repr__(self) -> str:
        return f"<TopCategory id={self.id} name={self.name} is_top={self.is_top}>"
