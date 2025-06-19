import os
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv

env_path = (
    Path(__file__).parent.parent.parent.parent / ".env"
)

load_dotenv(dotenv_path=env_path)


class Settings:
    APP_NAME: str = "sea-api"
    APP_VERSION: str = "0.0.1"
    MARKETING_NAME: str = "3D-Fans"
    COMPANY_NAME: str = "Make a Vision"

    POSTGRES_USER: str = os.getenv("DB_USER")
    POSTGRES_PASSWORD = urllib.parse.quote(
        os.getenv("DB_PASS", "")
    )
    POSTGRES_SERVER: str = os.getenv("DB_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "DB_PORT", 5432
    )  # default postgres port is 5432
    POSTGRES_DB: str = os.getenv("DB_NAME", "default")
    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        + f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    DATABASE_URL = DATABASE_URL.replace("%", "%%")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # in mins

    TEST_USER_EMAIL = "test@example.com"

    SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD")

    FORGOT_PASSWORD_TOKEN_DURATION = 60 * 24

    MAIL_SERVER: str = os.getenv(
        "MAIL_SERVER", "smtp.example.com"
    )
    MAIL_PORT = os.getenv("MAIL_PORT", 456)
    MAIL_USER = os.getenv("MAIL_USER", "default_user")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "example")
    MAIL_FROM = os.getenv(
        "MAIL_FROM", "default@example.com"
    )
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "example")

    API_BASE_URL = os.getenv("API_BASE_URL", "")

    WEB_APP_BASE_URL = os.getenv("WEB_APP_BASE_URL", "")

    CI = bool(os.getenv("CI", False))

    TEST_DATABASE_URL = "sqlite:///./test_db.db"

    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*").split(
        ","
    )
    STORAGE_PROVIDER = os.getenv(
        "STORAGE_PROVIDER", "minio"
    )
    STORAGE_ENDPOINT_URL = os.getenv("STORAGE_ENDPOINT_URL")
    STORAGE_ACCESS_KEY = os.getenv("STORAGE_ACCESS_KEY")
    STORAGE_SECRET_KEY = os.getenv("STORAGE_SECRET_KEY")
    STORAGE_BUCKET = os.getenv("STORAGE_BUCKET")


settings = Settings()


def get_database_uri() -> str:
    return settings.DATABASE_URL
