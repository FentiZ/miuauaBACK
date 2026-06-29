from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.data.base import Base


class DownCategory(Base):
    """
    Горизонтальная прокручиваемая лента категорий внутри контентной секции
    (например, фильтр под заголовком «Лідери продажу»).

    Каждый элемент ленты может быть привязан к конкретной TopCategory,
    чтобы лента отображалась только при активной вкладке.
    """
    __tablename__ = "down_categories"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String(255), nullable=False)
    slug            = Column(String(255), unique=True, index=True, nullable=False)
    description     = Column(Text, nullable=True)
    image_url       = Column(String(500), nullable=True)
    sort_order      = Column(Integer, default=0)
    is_active       = Column(Boolean, default=True)

    # К какой TopCategory относится эта лента-вкладка
    top_category_id = Column(Integer, ForeignKey("top_categories.id"), nullable=True)
    top_category    = relationship("TopCategory", backref="down_categories")

    # Опциональная ссылка на «настоящую» категорию каталога
    category_id     = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category        = relationship("Category", backref="down_entries")

    def __repr__(self) -> str:
        return f"<DownCategory id={self.id} name={self.name}>"
