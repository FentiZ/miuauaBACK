# MVP Backend — Auth + Products

**Python / FastAPI / SQLAlchemy / JWT**

## Архитектура: MVC

```
app/
├── models/           # M — SQLAlchemy-модели (таблицы БД)
│   ├── user.py
│   └── product.py
├── views/            # V — Pydantic-схемы (валидация + сериализация)
│   ├── auth_schemas.py
│   └── product_schemas.py
├── controllers/      # C — Бизнес-логика
│   ├── auth_controller.py
│   └── product_controller.py
├── routers/          # HTTP-слой (маршруты → контроллеры)
│   ├── auth_router.py
│   └── product_router.py
├── middleware/       # JWT-авторизация
│   └── auth.py
├── utils/            # JWT encode/decode, bcrypt
│   └── security.py
├── database/         # SQLAlchemy session, Base
│   └── base.py
└── main.py           # FastAPI app entry point
```

## Запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs

## API

### Auth
| Метод | URL | Auth | Описание |
|-------|-----|------|----------|
| POST | /auth/register | — | Регистрация |
| POST | /auth/login | — | Логин, возвращает JWT |
| GET | /auth/me | ✅ Bearer | Текущий пользователь |

### Products
| Метод | URL | Auth | Описание |
|-------|-----|------|----------|
| POST | /products/ | ✅ | Создать продукт |
| GET | /products/search | — | Поиск с фильтрами |
| GET | /products/my | ✅ | Мои продукты |
| GET | /products/{id} | — | Продукт по ID |
| PATCH | /products/{id} | ✅ | Обновить (только владелец) |
| DELETE | /products/{id} | ✅ | Soft-delete (только владелец) |

### Параметры поиска `/products/search`
- `query` — текстовый поиск по name + description
- `category` — фильтр по категории
- `min_price` / `max_price` — диапазон цены
- `in_stock` — true/false — наличие на складе
- `page` / `page_size` — пагинация

## Разбивка на микросервисы (следующий шаг)

```
auth-service/         ← models/user + controllers/auth + routers/auth
  └── PostgreSQL DB (users)

product-service/      ← models/product + controllers/product + routers/product
  └── PostgreSQL DB (products)

api-gateway/          ← nginx или FastAPI proxy
  └── маршрутизация между сервисами

Связь: REST или gRPC между сервисами
Auth: product-service делает HTTP-запрос в auth-service для верификации токена
      (или общий секрет JWT без межсервисного запроса)
```

## TODO (следующие итерации)
- [ ] Alembic-миграции (вместо `create_all`)
- [ ] Замена SQLite → PostgreSQL
- [ ] Email-верификация (`is_verified`)
- [ ] Refresh-токены
- [ ] Rate limiting
- [ ] Docker + docker-compose
- [ ] Тесты (pytest)
