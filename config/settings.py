
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    default_language: str = "en"
    mongo_url: str = 'localhost:27017'
    mongo_db_name: str = "bot"
    logs_channel: int | None = None

    class Config:
        env_file = "data/config.example.env"
        env_file_encoding = "utf-8"


config = Settings()
