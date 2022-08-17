"""This module implements the schemas for topics."""
from typing import List

from bson.objectid import ObjectId  # type: ignore
from pydantic import BaseModel, Field


class topic_model(BaseModel):
    """A single topic.

    Args:
        BaseModel (Any): Base class of FastAPI models.
    """

    id: str = Field(...)
    name: str = Field(...)
    keywords: List[str] = Field(...)
    score: float = Field(...)
    paper_ids: List[str] = Field(...)


class topic_response_model(BaseModel):
    """The model for a topic.

    Args:
        BaseModel (Any): Base class of FastAPI models.
    """

    topics: List[topic_model] = Field(...)

    # TODO: Adjust models and add fields that make sense

    class Config:
        """Configuration for the paper_model."""

        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "topics": [
                    {
                        "id": "5136bc054aed4daf9e2a1237",
                        "name": "Topic 1",
                        "score": 0.5,
                        "keywords": ["keyword 1", "keyword 2"],
                        "paper_ids": ["5136bc054aed4daf9e2a1239", "5136bc054aed4daf9e2a1238"],
                    },
                ],
            }
        }
