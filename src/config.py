import os

from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / 'db.sqlite3'


class DbSettings(BaseModel):
    '''Класс настроек для подключения к бд.'''
    url: str = f'{os.getenv("DB_URL")}:///{DB_PATH}'
    echo: bool = True  # для отладки


class Settings(BaseSettings):
    '''Класс настроек проекта.'''
    api_v1_prefix: str = '/api/v1'

    db: DbSettings = DbSettings()


settings = Settings()
