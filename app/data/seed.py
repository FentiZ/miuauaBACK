from sqlalchemy.orm import Session

from app.data.user import User, UserRole
from app.data.category import Category
from app.data.brand import Brand
from app.data.product import Product
from app.data.product_image import ProductImage
from app.data.product_spec import ProductSpecification
from app.utils.security import hash_password

def seed_database(db: Session) -> None:
    if db.query(Category).count() > 0:
        return

    admin = User(
        email="admin@mi-shop.ua",
        username="admin",
        full_name="Администратор магазина",
        hashed_password=hash_password("Admin12345"),
        role=UserRole.ADMIN,
        is_verified=True,
    )
    db.add(admin)
    db.flush()

    brands = {
        "xiaomi": Brand(name="Xiaomi", slug="xiaomi", logo_url="https://placehold.co/120x40?text=Xiaomi"),
        "redmi": Brand(name="Redmi", slug="redmi", logo_url="https://placehold.co/120x40?text=Redmi"),
        "poco": Brand(name="POCO", slug="poco", logo_url="https://placehold.co/120x40?text=POCO"),
        "mijia": Brand(name="Mijia", slug="mijia", logo_url="https://placehold.co/120x40?text=Mijia"),
    }
    for b in brands.values():
        db.add(b)
    db.flush()

    top = {
        "smartfony": Category(name="Смартфоны", slug="smartfony", sort_order=1,
                               image_url="https://placehold.co/64x64?text=Phone"),
        "smart-chasy-i-braslety": Category(name="Смарт-часы и браслеты", slug="smart-chasy-i-braslety", sort_order=2,
                                            image_url="https://placehold.co/64x64?text=Watch"),
        "noutbuki-i-planshety": Category(name="Ноутбуки и планшеты", slug="noutbuki-i-planshety", sort_order=3,
                                          image_url="https://placehold.co/64x64?text=Laptop"),
        "televizory-i-multimedia": Category(name="Телевизоры и мультимедиа", slug="televizory-i-multimedia", sort_order=4,
                                             image_url="https://placehold.co/64x64?text=TV"),
        "audio": Category(name="Аудио", slug="audio", sort_order=5,
                           image_url="https://placehold.co/64x64?text=Audio"),
        "bytovaya-tehnika": Category(name="Бытовая техника", slug="bytovaya-tehnika", sort_order=6,
                                      image_url="https://placehold.co/64x64?text=Home"),
        "stil-zhizni": Category(name="Стиль жизни", slug="stil-zhizni", sort_order=7,
                                 image_url="https://placehold.co/64x64?text=Style"),
    }
    for c in top.values():
        db.add(c)
    db.flush()

    sub = {
        "televizory": Category(name="Телевизоры", slug="televizory", parent_id=top["televizory-i-multimedia"].id, sort_order=1),
        "naushniki": Category(name="Наушники", slug="naushniki", parent_id=top["audio"].id, sort_order=1),
        "smart-chasy": Category(name="Смарт-часы", slug="smart-chasy", parent_id=top["smart-chasy-i-braslety"].id, sort_order=1),
        "noutbuki": Category(name="Ноутбуки", slug="noutbuki", parent_id=top["noutbuki-i-planshety"].id, sort_order=1),
        "roboty-pylesosy": Category(name="Роботы-пылесосы", slug="roboty-pylesosy", parent_id=top["bytovaya-tehnika"].id, sort_order=1),
        "universalnye-batarei": Category(name="Портативные батареи", slug="universalnye-batarei", parent_id=top["stil-zhizni"].id, sort_order=1),
    }
    for c in sub.values():
        db.add(c)
    db.flush()

    tv = Product(
        name="Телевизор Xiaomi TV S Mini LED 65 2026",
        slug="televizor-xiaomi-tv-s-mini-led-65-2026",
        short_description="65\" QLED Mini LED, Google TV, 144 Гц",
        description=(
            "Телевизор Xiaomi TV S Mini LED 65 2026 с экраном 65 дюймов, "
            "технологией Mini LED, поддержкой Dolby Vision и Google TV на борту."
        ),
        price=37999, old_price=49999,
        sku="TV-S-MINILED-65-2026",
        stock=12,
        category_id=sub["televizory"].id,
        brand_id=brands["xiaomi"].id,
        is_new=True, is_top=True,
        loyalty_partner="Fishka",
        review_bonus_points=300,
        rating_avg=5.0, reviews_count=5,
    )
    db.add(tv)
    db.flush()
    db.add_all([
        ProductImage(product_id=tv.id, image_url="https://placehold.co/600x400?text=Xiaomi+TV+S+65", is_main=True, sort_order=0),
        ProductImage(product_id=tv.id, image_url="https://placehold.co/600x400?text=TV+Back+Panel", sort_order=1),
    ])
    db.add_all([
        ProductSpecification(product_id=tv.id, group_name="Экран", name="Диагональ", value="65\"", sort_order=0),
        ProductSpecification(product_id=tv.id, group_name="Экран", name="Тип матрицы", value="QLED Mini LED", sort_order=1),
        ProductSpecification(product_id=tv.id, group_name="Экран", name="Разрешение", value="4K Ultra HD", sort_order=2),
        ProductSpecification(product_id=tv.id, group_name="Экран", name="Частота обновления", value="144 Гц", sort_order=3),
        ProductSpecification(product_id=tv.id, group_name="Звук", name="Мощность", value="30 Вт (2.0)", sort_order=4),
        ProductSpecification(product_id=tv.id, group_name="Платформа", name="Операционная система", value="Google TV", sort_order=5),
    ])

    smartphone = Product(
        name="Xiaomi 17T Pro 12/256GB Deep Violet",
        slug="xiaomi-17t-pro-12-256gb-deep-violet",
        short_description="12/256 ГБ, AMOLED 120 Гц, тройная камера 50 Мп",
        description="Флагманский смартфон Xiaomi 17T Pro с экраном AMOLED 120 Гц и быстрой зарядкой 120 Вт.",
        price=36499, old_price=38999,
        sku="XM-17T-PRO-12-256-DV",
        stock=25,
        category_id=top["smartfony"].id,
        brand_id=brands["xiaomi"].id,
        is_new=True, is_top=True,
        loyalty_partner="Fishka",
        review_bonus_points=300,
        rating_avg=4.9, reviews_count=11,
    )
    db.add(smartphone)
    db.flush()
    db.add_all([
        ProductImage(product_id=smartphone.id, image_url="https://placehold.co/600x400?text=Xiaomi+17T+Pro", color_name="Deep Violet", color_hex="#4B3B6B", is_main=True, sort_order=0),
        ProductImage(product_id=smartphone.id, image_url="https://placehold.co/600x400?text=Xiaomi+17T+Pro+Blue", color_name="Deep Blue", color_hex="#1E3A8A", sort_order=1),
    ])
    db.add_all([
        ProductSpecification(product_id=smartphone.id, group_name="Экран", name="Диагональ", value="6.83\"", sort_order=0),
        ProductSpecification(product_id=smartphone.id, group_name="Экран", name="Частота обновления", value="120 Гц", sort_order=1),
        ProductSpecification(product_id=smartphone.id, group_name="Память", name="ОЗУ / встроенная память", value="12/256 ГБ", sort_order=2),
        ProductSpecification(product_id=smartphone.id, group_name="Камера", name="Основная камера", value="50 Мп, тройная", sort_order=3),
        ProductSpecification(product_id=smartphone.id, group_name="Батарея", name="Ёмкость", value="5500 мАч, 120 Вт", sort_order=4),
    ])

    vacuum = Product(
        name="Робот-пылесос Xiaomi Robot Vacuum X20 Pro",
        slug="robot-pylesos-xiaomi-robot-vacuum-x20-pro",
        short_description="Влажная уборка, лазерная навигация LDS, 6000 Па",
        price=18999, old_price=29999,
        sku="XM-VACUUM-X20-PRO",
        stock=8,
        category_id=sub["roboty-pylesosy"].id,
        brand_id=brands["xiaomi"].id,
        is_top=True,
        rating_avg=5.0, reviews_count=5,
    )
    db.add(vacuum)
    db.flush()
    db.add(ProductImage(product_id=vacuum.id, image_url="https://placehold.co/600x400?text=Robot+Vacuum+X20+Pro", is_main=True))
    db.add(ProductSpecification(product_id=vacuum.id, group_name="Уборка", name="Мощность всасывания", value="6000 Па", sort_order=0))

    earbuds = Product(
        name="Наушники Xiaomi OpenWear Stereo Golden",
        slug="naushniki-xiaomi-openwear-stereo-golden",
        short_description="Открытый тип, Bluetooth 5.4, до 28 часов работы",
        price=3999, old_price=6699,
        sku="XM-OPENWEAR-GOLD",
        stock=40,
        category_id=sub["naushniki"].id,
        brand_id=brands["xiaomi"].id,
        is_new=True,
        rating_avg=4.7, reviews_count=4,
    )
    db.add(earbuds)
    db.flush()
    db.add(ProductImage(product_id=earbuds.id, image_url="https://placehold.co/600x400?text=OpenWear+Stereo", is_main=True))

    poco_phone = Product(
        name="POCO X7 Pro 12/256GB Black",
        slug="poco-x7-pro-12-256gb-black",
        short_description="Dimensity 8400 Ultra, 90 Вт зарядка",
        price=12999,
        sku="POCO-X7-PRO-12-256-BLK",
        stock=15,
        category_id=top["smartfony"].id,
        brand_id=brands["poco"].id,
        is_new=True,
        rating_avg=0, reviews_count=0,
    )
    db.add(poco_phone)
    db.flush()
    db.add(ProductImage(product_id=poco_phone.id, image_url="https://placehold.co/600x400?text=POCO+X7+Pro", is_main=True))

    db.commit()
