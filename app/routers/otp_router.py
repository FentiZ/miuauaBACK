from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.data.base import get_db
from app.dto.otp_schemas import OtpSendRequest, OtpVerifyRequest, OtpSendResponse
from app.dto.auth_schemas import TokenResponse
from app.controllers.otp_controller import OtpController

router = APIRouter(prefix="/auth/otp", tags=["Auth — OTP (Email)"])


@router.post(
    "/send",
    response_model=OtpSendResponse,
    summary="Отправить OTP-код на email",
    description=(
        "Генерирует 6-значный код и отправляет на указанный email. "
        "Код действителен 10 минут. Повторный вызов аннулирует предыдущий код."
    ),
)
def send_otp(payload: OtpSendRequest, db: Session = Depends(get_db)):
    return OtpController.send_otp(payload, db)


@router.post(
    "/verify",
    response_model=TokenResponse,
    summary="Подтвердить OTP-код → получить токены",
    description=(
        "Принимает email + 6-значный код. "
        "Если пользователь с таким email не существует — создаёт его автоматически. "
        "Возвращает access_token + refresh_token."
    ),
)
def verify_otp(payload: OtpVerifyRequest, db: Session = Depends(get_db)):
    return OtpController.verify_otp(payload, db)
