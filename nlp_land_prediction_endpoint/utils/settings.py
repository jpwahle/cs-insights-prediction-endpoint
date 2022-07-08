"""This module implements the settings as well as the default settings"""
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class according to pydantic"""

    AUTH_BACKEND_VERSION: Optional[str] = "v0"
    AUTH_BACKEND_URL: str = "http://127.0.0.1/api/{version}"
    AUTH_BACKEND_LOGIN_ROUTE: str = "/auth/login/service"
    AUTH_TOKEN_ROUTE: str = "/auth/service"
    JWT_SECRET: str = "super_secret_secret"
    JWT_TOKEN_EXPIRATION_MINUTES: int = 30
    JWT_SIGN_ALG: str = "HS256"
    NODE_TYPE: str = "SECONDARY"

    class Config:
        """Configuration for settings"""

        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Return the Settings object"""
    return Settings()
