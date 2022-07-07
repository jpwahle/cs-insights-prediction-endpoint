from pydantic import BaseSettings
from functools import lru_cache

from functools import lru_cache
class Settings(BaseSettings):
    AUTH_BACKEND_VERSION: str = "v0"
    AUTH_BACKEND_URL:str = "http://127.0.0.1/api/{version}"
    AUTH_BACKEND_LOGIN_ROUTE: str ="/auth/login/service"
    AUTH_TOKEN_ROUTE: str = "/auth/service"
    JWT_SECRET:str = "super_secret_secret"
    JWT_TOKEN_EXPIRATION_MINUTES: int = 30
    JWT_SIGN_ALG: str = "HS256"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

