import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.data.user import User
from app.dto.auth_schemas import (
    UserRegisterRequest, UserLoginRequest, UserUpdateRequest, ChangePasswordRequest,
    TokenResponse, UserResponse, MessageResponse,
)
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)


def _build_token_response(user: User) -> TokenResponse:
    sub = {"sub": str(user.id)}
    return TokenResponse(
        access_token=create_access_token(sub),
        refresh_token=create_refresh_token(sub),
        user=UserResponse.model_validate(user),
    )


def _generate_username(db: Session) -> str:
    """Генерирует уникальный username вида user_<8 символов>."""
    while True:
        candidate = "user_" + uuid.uuid4().hex[:8]
        if not db.query(User).filter(User.username == candidate).first():
            return candidate


class AuthController:

    # ──────────────────────────────────────────
    # Register
    # ──────────────────────────────────────────

    @staticmethod
    def register(payload: UserRegisterRequest, db: Session) -> TokenResponse:
        # Проверяем уникальность email
        if payload.email:
            if db.query(User).filter(User.email == payload.email).first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email уже зарегистрирован",
                )

        # Проверяем уникальность телефона
        if payload.phone:
            if db.query(User).filter(User.phone == payload.phone).first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Телефон уже зарегистрирован",
                )

        user = User(
            email=payload.email or None,
            username=_generate_username(db),
            phone=payload.phone or None,
            full_name=payload.full_name,
            hashed_password=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return _build_token_response(user)

    # ──────────────────────────────────────────
    # Login  (email ИЛИ телефон)
    # ──────────────────────────────────────────

    @staticmethod
    def login(payload: UserLoginRequest, db: Session) -> TokenResponse:
        user = None

        # Пробуем найти по email
        if payload.login_as_email:
            user = db.query(User).filter(User.email == payload.login_as_email).first()

        # Пробуем найти по телефону
        if user is None and payload.login_as_phone:
            user = db.query(User).filter(User.phone == payload.login_as_phone).first()

        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email/телефон или пароль",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт деактивирован",
            )
        return _build_token_response(user)

    # ──────────────────────────────────────────
    # Refresh
    # ──────────────────────────────────────────

    @staticmethod
    def refresh(refresh_token: str, db: Session) -> TokenResponse:
        payload = decode_token(refresh_token, expected_type="refresh")
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный или истёкший refresh-токен",
            )
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден",
            )
        return _build_token_response(user)

    # ──────────────────────────────────────────
    # Me
    # ──────────────────────────────────────────

    @staticmethod
    def get_me(current_user: User) -> UserResponse:
        return UserResponse.model_validate(current_user)

    @staticmethod
    def update_me(payload: UserUpdateRequest, current_user: User, db: Session) -> UserResponse:
        if payload.phone and payload.phone != current_user.phone:
            if db.query(User).filter(
                User.phone == payload.phone, User.id != current_user.id
            ).first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Телефон уже используется",
                )
        if payload.email and payload.email != current_user.email:
            if db.query(User).filter(
                User.email == payload.email, User.id != current_user.id
            ).first():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email уже используется",
                )

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(current_user, field, value)
        db.commit()
        db.refresh(current_user)
        return UserResponse.model_validate(current_user)

    @staticmethod
    def change_password(
        payload: ChangePasswordRequest, current_user: User, db: Session
    ) -> MessageResponse:
        if not verify_password(payload.old_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный текущий пароль",
            )
        current_user.hashed_password = hash_password(payload.new_password)
        db.commit()
        return MessageResponse(message="Пароль успешно изменён")
