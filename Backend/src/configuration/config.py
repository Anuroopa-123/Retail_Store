# src/configuration/config.py

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # ── App ───────────────────────────────────────────────────────────────────
    APP_NAME: str = "Retail Store API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # ── Database ──────────────────────────────────────────────────────────────
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int = 5432

    # ── JWT ───────────────────────────────────────────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── App URLs & Env ────────────────────────────────────────────────────────
    API_URL: str = "http://127.0.0.1:8000"
    APP_URL: str = "http://127.0.0.1:8000"
    APP_ENV: str = "development"
    ALLOWED_HOSTS: str = "*"

    # ── Mail ──────────────────────────────────────────────────────────────────
    MAIL_HOST: str = "sandbox.smtp.mailtrap.io"
    MAIL_PORT: int = 2525
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str = "noreply@retailstore.com"
    MAIL_FROM_NAME: str = "RetailStore"
    
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def CORS_ORIGINS_LIST(self):
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
        ]

    @property
    def ALLOWED_HOSTS_LIST(self) -> list[str]:
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]

    @property
    def DB_KWARGS(self) -> dict:
        return {
            "DB_USERNAME": self.DB_USERNAME,
            "DB_PASSWORD": self.DB_PASSWORD,
            "DB_HOST": self.DB_HOST,
            "DB_NAME": self.DB_NAME,
            "DB_PORT": self.DB_PORT,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Config()