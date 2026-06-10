from fastapi_mail import FastMail, MessageSchema, MessageType
from src.infrastructure.mail import conf, get_email_css
from src.configuration.config import config

fm = FastMail(conf)


class EmailService:

    @staticmethod
    async def send_verification_email(to: str, token: str) -> None:
        link = f"{config.APP_URL}/verify-email?token={token}"
        css = get_email_css()
        message = MessageSchema(
        subject="Verify Email",
        recipients=[to],
        body=f"""
        <html>
        <body>
        <div style="font-family:Arial">

        <h2>Email Verification</h2>

        <p>Your verification code is:</p>

        <h1>{token}</h1>

        <p>Expires in 24 hours.</p>

        </div>
        </body>
        </html>
        """,
            subtype=MessageType.html,
        )
        await fm.send_message(message)

    @staticmethod
    async def send_password_reset_email(to: str, token: str) -> None:
        link = f"{config.APP_URL}/api/v1/auth/reset-password?token={token}"
        css = get_email_css()
        message = MessageSchema(
            subject="Reset your password",
            recipients=[to],
            body=f"""
            <html><head><style>{css}</style></head>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
                    <h2>Reset your password</h2>
                    <p>Click below to reset your password.</p>
                    <a href="{link}"
                       style="display:inline-block; padding:12px 24px; background:#4F46E5;
                              color:#fff; border-radius:6px; text-decoration:none;">
                        Reset Password
                    </a>
                    <p style="margin-top:16px; color:#6B7280; font-size:13px;">
                        Expires in 1 hour. If you didn't request this, ignore this.
                    </p>
                </div>
            </body></html>
            """,
            subtype=MessageType.html,
        )
        await fm.send_message(message)