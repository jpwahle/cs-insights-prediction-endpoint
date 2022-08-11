"""This module implements the models for remote hosts"""
from typing import List, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound="RemoteHost")


class RemoteHost(BaseModel):
    """The model for a Remote Host

    Args:
        BaseModel (Any): Base class of FastAPI models.
    """

    ip: str = Field(...)
    port: str = Field(...)
    # token: str # Authentication token
    models: List[str] = Field(...)  # List of possible models (names like lda)
    created_models: List[str]  # List of actual created models (ids)
