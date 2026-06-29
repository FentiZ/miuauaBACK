import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args)

@event.listens_for(engine, "connect")
def _register_unicode_lower(dbapi_connection, connection_record):

    if DATABASE_URL.startswith("sqlite"):
        dbapi_connection.create_function(
            "lower", 1, lambda s: s.lower() if s is not None else s
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
