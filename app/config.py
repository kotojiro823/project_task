# app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    jwt_secret: str

    class Config:
        env_file = ".env"

settings = Settings()
