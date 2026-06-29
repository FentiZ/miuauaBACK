"""
Отправка SMS через Twilio.

Для работы нужно:
1. Зарегистрироваться на twilio.com и получить триал-аккаунт (бесплатно).
2. В Twilio Console взять:
   - Account SID  → TWILIO_ACCOUNT_SID
   - Auth Token   → TWILIO_AUTH_TOKEN
   - Номер-отправитель (Phone Number) → TWILIO_FROM_PHONE
3. Прописать переменные в .env
4. pip install twilio
"""
from app.core.config import settings


class SmsService:

    def send_otp(self, to_phone: str, code: str, expire_minutes: int) -> None:
        """Отправить SMS с OTP-кодом."""
        # Ленивый импорт — если twilio не установлен, ошибка будет только при вызове
        try:
            from twilio.rest import Client
        except ImportError:
            raise RuntimeError(
                "Пакет twilio не установлен. Выполните: pip install twilio"
            )

        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            raise RuntimeError(
                "Не заданы TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN в .env"
            )
        if not settings.TWILIO_FROM_PHONE:
            raise RuntimeError(
                "Не задан TWILIO_FROM_PHONE в .env"
            )

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        body = (
            f"Ваш код подтверждения: {code}\n"
            f"Код действителен {expire_minutes} мин. Не сообщайте его никому."
        )
        client.messages.create(
            body=body,
            from_=settings.TWILIO_FROM_PHONE,
            to=to_phone,
        )


sms_service = SmsService()
