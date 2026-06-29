from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.data.base import Base


class BackCategory(Base):
    """
    Боковое (левое) меню с иконками — «Смартфони», «Смарт-годинники та браслети» … (Скрин 2).

    icon_name   — имя иконки (например, имя SVG-файла или ключ иконочного шрифта).
    icon_url    — прямая ссылка на SVG/PNG-иконку (альтернатива icon_name).
    Используйте одно из двух, либо оба.
    """
    __tablename__ = "back_categories"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(255), nullable=False)
    slug        = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    icon_name   = Column(String(255), nullable=True)   # ключ иконки
    icon_url    = Column(String(500), nullable=True)   # URL иконки
    sort_order  = Column(Integer, default=0)
    is_active   = Column(Boolean, default=True)

    # Опциональная ссылка на «настоящую» категорию каталога
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category    = relationship("Category", backref="back_entries")

    # Дочерние подпункты бокового меню
    parent_id   = Column(Integer, ForeignKey("back_categories.id"), nullable=True)
    parent      = relationship("BackCategory", remote_side=[id], back_populates="children")
    children    = relationship("BackCategory", back_populates="parent", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<BackCategory id={self.id} name={self.name}>"
