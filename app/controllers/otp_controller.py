import random
import string
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.data.otp import EmailOtp, PhoneOtp
from app.data.user import User
from app.dto.otp_schemas import OtpSendRequest, OtpVerifyRequest, OtpSendResponse
from app.dto.auth_schemas import TokenResponse
from app.utils.email import email_service
from app.utils.sms import sms_service
from app.controllers.auth_controller import _build_token_response, _generate_username


def _generate_code(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))


class OtpController:

    # ──────────────────────────────────────────
    # Отправить OTP (email или phone)
    # ──────────────────────────────────────────

    @staticmethod
    def send_otp(payload: OtpSendRequest, db: Session) -> OtpSendResponse:
        code = _generate_code()
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)

        if payload.email:
            # Инвалидируем старые коды для этого email
            db.query(EmailOtp).filter(
                EmailOtp.email == payload.email,
                EmailOtp.is_used == False,
            ).delete()
            db.commit()

            otp = EmailOtp(
                email=payload.email,
                code=code,
                expires_at=expires_at,
            )
            db.add(otp)
            db.commit()

            try:
                email_service.send_otp(payload.email, code, settings.OTP_EXPIRE_MINUTES)
            except Exception as e:
                db.delete(otp)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Не удалось отправить письмо: {str(e)}",
                )

            return OtpSendResponse(
                message=f"Код отправлен на {payload.email}",
                expires_in_minutes=settings.OTP_EXPIRE_MINUTES,
            )

        else:  # payload.phone
            # Инвалидируем старые коды для этого телефона
            db.query(PhoneOtp).filter(
                PhoneOtp.phone == payload.phone,
                PhoneOtp.is_used == False,
            ).delete()
            db.commit()

            otp = PhoneOtp(
                phone=payload.phone,
                code=code,
                expires_at=expires_at,
            )
            db.add(otp)
            db.commit()

            try:
                sms_service.send_otp(payload.phone, code, settings.OTP_EXPIRE_MINUTES)
            except Exception as e:
                db.delete(otp)
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Не удалось отправить SMS: {str(e)}",
                )

            return OtpSendResponse(
                message=f"Код отправлен на {payload.phone}",
                expires_in_minutes=settings.OTP_EXPIRE_MINUTES,
            )

    # ──────────────────────────────────────────
    # Проверить OTP → вернуть JWT токены
    # ──────────────────────────────────────────

    @staticmethod
    def verify_otp(payload: OtpVerifyRequest, db: Session) -> TokenResponse:
        if payload.email:
            return OtpController._verify_email_otp(payload, db)
        else:
            return OtpController._verify_phone_otp(payload, db)

    @staticmethod
    def _verify_email_otp(payload: OtpVerifyRequest, db: Session) -> TokenResponse:
        otp = (
            db.query(EmailOtp)
            .filter(
                EmailOtp.email == payload.email,
                EmailOtp.code == payload.code,
                EmailOtp.is_used == False,
            )
            .order_by(EmailOtp.created_at.desc())
            .first()
        )

        if otp is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный код подтверждения",
            )
        if datetime.utcnow() > otp.expires_at:
            otp.is_used = True
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Срок действия кода истёк. Запросите новый.",
            )

        otp.is_used = True
        db.commit()

        user = db.query(User).filter(User.email == payload.email).first()

        if user is None:
            user = User(
                email=payload.email,
                username=_generate_username(db),
                hashed_password="",
                is_verified=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            try:
                email_service.send_welcome(payload.email, user.full_name)
            except Exception:
                pass
        elif not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт деактивирован",
            )
        else:
            if not user.is_verified:
                user.is_verified = True
                db.commit()

        return _build_token_response(user)

    @staticmethod
    def _verify_phone_otp(payload: OtpVerifyRequest, db: Session) -> TokenResponse:
        otp = (
            db.query(PhoneOtp)
            .filter(
                PhoneOtp.phone == payload.phone,
                PhoneOtp.code == payload.code,
                PhoneOtp.is_used == False,
            )
            .order_by(PhoneOtp.created_at.desc())
            .first()
        )

        if otp is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный код подтверждения",
            )
        if datetime.utcnow() > otp.expires_at:
            otp.is_used = True
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Срок действия кода истёк. Запросите новый.",
            )

        otp.is_used = True
        db.commit()

        user = db.query(User).filter(User.phone == payload.phone).first()

        if user is None:
            # Авторегистрация по телефону
            user = User(
                phone=payload.phone,
                username=_generate_username(db),
                hashed_password="",
                is_verified=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        elif not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт деактивирован",
            )
        else:
            if not user.is_verified:
                user.is_verified = True
                db.commit()

        return _build_token_response(user)
