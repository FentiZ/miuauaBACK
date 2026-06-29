from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.data.base import Base, engine, SessionLocal
from app.data import *
from app.data.seed import seed_database
from app.routers import (
    auth_router, product_router, category_router, brand_router,
    upload_router, search_router, top_category_router,
    back_category_router, down_category_router, cart_router,
)
from app.routers.otp_router import router as otp_router
from app.search.client import ensure_all_indices
from app.search.config import ES_INDICES

Base.metadata.create_all(bind=engine)

with SessionLocal() as _db:
    seed_database(_db)

ensure_all_indices(ES_INDICES)

app = FastAPI(title="Shop Backend", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(otp_router)
app.include_router(category_router.router)
app.include_router(brand_router.router)
app.include_router(product_router.router)
app.include_router(upload_router.router)
app.include_router(search_router.router)
app.include_router(top_category_router.router)
app.include_router(back_category_router.router)
app.include_router(down_category_router.router)
app.include_router(cart_router.router)

_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.exists():
    app.mount("/demo", StaticFiles(directory=str(_frontend_dir), html=True), name="demo")

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
