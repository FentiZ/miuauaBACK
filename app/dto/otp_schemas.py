from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
import re


def _normalize_email(v: str) -> str:
    v = v.strip().lower()
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", v):
        raise ValueError("Некорректный формат email")
    return v


def _normalize_phone(v: str) -> str:
    """Приводит номер к формату +380XXXXXXXXX."""
    digits = re.sub(r"\D", "", v)
    if len(digits) == 10:
        digits = "38" + digits
    if len(digits) == 12 and digits.startswith("38"):
        return "+" + digits
    raise ValueError("Телефон должен быть в формате +380XXXXXXXXX или 0XXXXXXXXX")


class OtpSendRequest(BaseModel):
    """
    Отправить OTP: укажите email ИЛИ phone (одно из двух обязательно).
    - email → код придёт письмом
    - phone → код придёт SMS (через Twilio)
    """
    email: Optional[str] = None
    phone: Optional[str] = None

    @model_validator(mode="after")
    def email_or_phone_required(self) -> "OtpSendRequest":
        if not self.email and not self.phone:
            raise ValueError("Укажите email или номер телефона")
        if self.email and self.phone:
            raise ValueError("Укажите только одно: email или телефон")
        return self

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        return _normalize_email(v)

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        return _normalize_phone(v.strip())


class OtpVerifyRequest(BaseModel):
    """
    Подтвердить OTP: тот же email/phone + 6-значный код.
    """
    email: Optional[str] = None
    phone: Optional[str] = None
    code: str

    @model_validator(mode="after")
    def email_or_phone_required(self) -> "OtpVerifyRequest":
        if not self.email and not self.phone:
            raise ValueError("Укажите email или номер телефона")
        if self.email and self.phone:
            raise ValueError("Укажите только одно: email или телефон")
        return self

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        return _normalize_email(v)

    @field_validator("phone")
    @classmethod
    def phone_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == "":
            return None
        return _normalize_phone(v.strip())

    @field_validator("code")
    @classmethod
    def code_valid(cls, v: str) -> str:
        v = v.strip()
        if not v.isdigit() or len(v) != 6:
            raise ValueError("Код должен состоять из 6 цифр")
        return v


class OtpSendResponse(BaseModel):
    message: str
    expires_in_minutes: int
