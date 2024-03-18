from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    # Debug should be set to False on production
    DEBUG: Optional[bool] = os.getenv("DEBUG") == "True"
    # Title is the name of application
    TITLE: Optional[str] = os.getenv("TITLE")
    # SQLITE connection string
    SQLITE_CONNECTION_STRING: Optional[str] = "sqlite:///database.db"  # os.getenv("SQLITE_CONNECTION_STRING")
    # JWT
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    # Origins
    ORIGINS: Optional[str] = os.getenv("ORIGINS")
    # Redis & Celery
    BROKER: Optional[str] = os.getenv("BROKER")
    BACKEND: Optional[str] = os.getenv("BACKEND")


settings = Settings()
