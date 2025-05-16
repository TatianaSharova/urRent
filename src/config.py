import os

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class RunAppConfig(BaseModel):
    """Класс настроек для запуска приложения."""

    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True


class ApiPrefix(BaseModel):
    """Класс настроек для префикса api."""

    v1: str = "/api/v1"


class DbSettings(BaseModel):
    """Класс настроек для подключения к бд."""

    url: str = f'{os.getenv("DB_URL")}:///{DB_PATH}'
    echo: bool = True  # для отладки
    naming_convention: dict = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    """Класс настроек проекта."""

    run: RunAppConfig = RunAppConfig()
    api_prefix: ApiPrefix = ApiPrefix()
    db: DbSettings = DbSettings()


settings = Settings()
