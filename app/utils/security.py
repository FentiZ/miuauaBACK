from datetime import datetime, timedelta, timezone
from typing import Optional, Literal
import os

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY: str = os.environ["SECRET_KEY"]
ALGORITHM: str  = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES: int  = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
REFRESH_TOKEN_EXPIRE_DAYS:   int  = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS",   "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def _create_token(
    data: dict,
    token_type: Literal["access", "refresh"],
    expires_delta: Optional[timedelta] = None,
) -> str:

    if expires_delta is None:
        if token_type == "access":
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    now = datetime.now(tz=timezone.utc)
    payload = {
        **data,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    return _create_token(data, "access", expires_delta)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    return _create_token(data, "refresh", expires_delta)

def decode_token(token: str, expected_type: Optional[Literal["access", "refresh"]] = None) -> Optional[dict]:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if expected_type and payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None
