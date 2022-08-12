"""This module implements the settings as well as the default settings"""
from functools import lru_cache

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """Settings class according to pydantic"""

    auth_backend_version: str = "v0"
    implemented_models: list = [
        {"lda": ["cs_insights_prediction_endpoint.models.lda_model", "LDAModel"]}
    ]
    node_type: str = "SECONDARY"
    remote_host_db_name: str = "remote_hosts"
    model_db_name: str = "models"
    auth_token_route: str = "/auth/service"
    auth_backend_login_route: str = "/auth/login/service"
    jwt_sign_alg: str = "HS256"
    jwt_token_expiration_minutes: int = 30

    jwt_secret: SecretStr
    mongo_user: SecretStr
    mongo_password: SecretStr
    mongo_db: str
    mongo_host: str
    auth_backend_url: str

    class Config:
        """Configuration for settings"""

        case_sensitive = False
        env_file = ".env.development"
        secrets_dir = "/run/secrets"  # for production and docker secrets


@lru_cache()
def get_settings() -> Settings:
    """Return the Settings object"""
    return Settings()
