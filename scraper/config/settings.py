import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME")
    MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING")


settings = Settings()
