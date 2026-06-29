from pydantic import BaseModel, EmailStr, field_validator, model_validator
from datetime import datetime
from typing import Optional
import re


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _normalize_phone(v: str) -> str:
    """Приводит номер к формату +380XXXXXXXXX."""
    digits = re.sub(r"\D", "", v)
    if len(digits) == 10:
        digits = "38" + digits
    if len(digits) == 12 and digits.startswith("38"):
        return "+" + digits
    raise ValueError("Телефон должен быть в формате +380XXXXXXXXX или 0XXXXXXXXX")


def _is_email(value: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))


def _is_phone(value: str) -> bool:
    return bool(re.match(r"^[+0-9()\s\-]{7,20}$", value))


# ──────────────────────────────────────────────
# Register
# ──────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    """
    Регистрация: email ИЛИ телефон (одно из двух обязательно).
    username генерируется автоматически — пользователю вводить не нужно.
    """
    email: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    password: str
    password_confirm: str

    @model_validator(mode="after")
    def email_or_phone_required(self) -> "UserRegisterRequest":
        if not self.email and not self.phone:
            raise ValueError("Укажите email или номер телефона")
        return self

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Некорректный формат email")
        return v

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        return _normalize_phone(v.strip())

    @field_validator("password")
    @classmethod
    def password_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль минимум 8 символов")
        return v

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return v


# ──────────────────────────────────────────────
# Login  (email ИЛИ телефон в одном поле)
# ──────────────────────────────────────────────

class UserLoginRequest(BaseModel):
    """
    Поле `login` принимает email или номер телефона — как на mi.ua.
    """
    login: str
    password: str

    @field_validator("login")
    @classmethod
    def login_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Введите email или телефон")
        if not _is_email(v) and not _is_phone(v):
            raise ValueError("Введите корректный email или номер телефона")
        return v

    # Удобное свойство: нормализованный телефон (если это телефон)
    @property
    def login_as_phone(self) -> Optional[str]:
        if _is_phone(self.login):
            try:
                return _normalize_phone(self.login)
            except Exception:
                return None
        return None

    @property
    def login_as_email(self) -> Optional[str]:
        return self.login.lower() if _is_email(self.login) else None


# ──────────────────────────────────────────────
# Other schemas (unchanged)
# ──────────────────────────────────────────────

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        return _normalize_phone(v.strip())

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        v = v.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Некорректный формат email")
        return v


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль минимум 8 символов")
        return v


class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("role", mode="before")
    @classmethod
    def role_to_str(cls, v):
        return v.value if hasattr(v, "value") else v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    message: str
    success: bool = True
