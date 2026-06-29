from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.data.base import Base


class EmailOtp(Base):
    __tablename__ = "email_otps"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String(255), index=True, nullable=False)
    code       = Column(String(6), nullable=False)
    is_used    = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmailOtp email={self.email} used={self.is_used}>"


class PhoneOtp(Base):
    """OTP-коды для входа по номеру телефона (через SMS)."""
    __tablename__ = "phone_otps"

    id         = Column(Integer, primary_key=True, index=True)
    phone      = Column(String(32), index=True, nullable=False)
    code       = Column(String(6), nullable=False)
    is_used    = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PhoneOtp phone={self.phone} used={self.is_used}>"
