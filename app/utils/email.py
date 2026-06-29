import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from app.core.config import settings


class EmailService:
    """
    Отправка писем через Gmail SMTP.

    Для работы нужно:
    1. Включить 2FA в Google-аккаунте.
    2. Создать App Password: Google Account → Security → App passwords.
    3. Прописать в .env:
       SMTP_USER=your@gmail.com
       SMTP_PASSWORD=xxxx xxxx xxxx xxxx   (16-символьный App Password)
    """

    def __init__(self):
        self.host     = settings.SMTP_HOST
        self.port     = settings.SMTP_PORT
        self.user     = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
        self.sender   = settings.SMTP_SENDER_NAME

    # ──────────────────────────────────────────
    # Низкоуровневая отправка
    # ──────────────────────────────────────────

    def send(self, to_email: str, subject: str, html_body: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{self.sender} <{self.user}>"
        msg["To"]      = to_email

        msg.attach(MIMEText(html_body, "html", "utf-8"))

        context = ssl.create_default_context()
        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(self.user, self.password)
            server.sendmail(self.user, to_email, msg.as_string())

    # ──────────────────────────────────────────
    # Готовые шаблоны
    # ──────────────────────────────────────────

    def send_otp(self, to_email: str, code: str, expires_minutes: int = 10) -> None:
        subject = "Ваш код подтверждения"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
            <h2 style="color: #1a1a1a;">Код подтверждения</h2>
            <p style="color: #444;">Введите этот код для входа в аккаунт:</p>
            <div style="
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 8px;
                color: #2563eb;
                background: #f0f4ff;
                border-radius: 8px;
                padding: 20px 32px;
                display: inline-block;
                margin: 16px 0;
            ">{code}</div>
            <p style="color: #888; font-size: 13px;">
                Код действителен {expires_minutes} минут.<br>
                Если вы не запрашивали этот код — просто проигнорируйте письмо.
            </p>
        </div>
        """
        self.send(to_email, subject, html)

    def send_welcome(self, to_email: str, full_name: Optional[str] = None) -> None:
        name = full_name or "пользователь"
        subject = "Добро пожаловать!"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
            <h2 style="color: #1a1a1a;">Привет, {name}! 👋</h2>
            <p style="color: #444;">Ваш аккаунт успешно создан. Рады видеть вас в нашем магазине!</p>
        </div>
        """
        self.send(to_email, subject, html)


# Singleton — используем один экземпляр во всём приложении
email_service = EmailService()
