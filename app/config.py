from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(dotenv_path=BASE_DIR / ".env")


class Settings(BaseSettings):
    debug: bool = Field(default=False)
    echo_active: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()


templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

UPLOAD_DIR = BASE_DIR / "uploads"

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
