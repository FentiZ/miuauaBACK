from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Database ──────────────────────────────
    DATABASE_URL: str = "sqlite:///./app.db"

    # ── JWT ───────────────────────────────────
    SECRET_KEY: str = "CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── SMTP (Gmail) ──────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""           # your@gmail.com
    SMTP_PASSWORD: str = ""       # 16-символьный App Password
    SMTP_SENDER_NAME: str = "My Shop"

    # ── OTP ───────────────────────────────────
    OTP_EXPIRE_MINUTES: int = 10

    # ── Twilio (SMS OTP) ──────────────────────
    TWILIO_ACCOUNT_SID: str = ""   # ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    TWILIO_AUTH_TOKEN: str = ""    # ваш Auth Token из Twilio Console
    TWILIO_FROM_PHONE: str = ""    # +1XXXXXXXXXX — номер-отправитель

    # ── AWS S3 ────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "eu-central-1"
    AWS_S3_BUCKET: str = ""
    AWS_S3_PUBLIC_URL: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
