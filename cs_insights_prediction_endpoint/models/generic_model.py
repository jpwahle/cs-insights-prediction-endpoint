"""This modulew implements the generic-model"""
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound="GenericModel")


class GenericModel(BaseModel):
    """Generic Model."""

    id: str
    name: str = Field(..., min_length=1, max_length=32)
    created_by: str = Field(...)
    created_at: float
    description: str = Field(...)
    # XXX-TN We should a GenericCreationParameters, same as GenericInputModel
    save_directory: str = "./saved_models"
    creation_parameters: Optional[dict] = {}
    type_of_model: str = Field(...)
    function_calls: dict = Field(...)
    processing_model: Any

    def __init__(self: T, **data: Any) -> None:
        """Constructor for GenericModel"""
        if "created_at" not in data:
            data["created_at"] = datetime.timestamp(datetime.now())
        if "id" not in data:
            data["id"] = str(hash(data["name"]))
        super().__init__(**data)
        Path(self.save_directory).mkdir(parents=True, exist_ok=True)

    def __str__(self: T) -> str:
        """Returns the String-representation of this GenericModel instance

        Returns:
            str: String representation of this GenericModel instance
        """
        return self.id

    def get_id(self: T) -> str:
        """Returns the id of the object

        Returns:
            str: The id of the current object
        """
        return self.id

    def get_name(self: T) -> str:
        """Returns the name of the object

        Returns:
            str: The name of the current object
        """
        return self.name

    def get_function_calls(self: T) -> list:
        """Returns the name of all the functions available

        Returns:
            list: Names of all implemented functions
        """
        return list(self.function_calls.keys())

    def train(self: T, input_object: dict) -> None:
        """Train the model with data from inputObject"""
        raise NotImplementedError("GenericModel.train has to be implemented by the subclass")

    def predict(self: T, input_object: dict) -> list:
        """Predict something with data from inputObject"""
        raise NotImplementedError("GenericModel.predict has to be implemented by the subclass")

    def save(self: T, path: str) -> None:
        """Function to save the state of the model"""
        raise NotImplementedError("GenericModel.save has to be implemented by the subclass")

    def load(self: T, path: str) -> None:
        """Function to load the state of the model"""
        raise NotImplementedError("GenericModel.load has to be implemented by the subclass")


class GenericInputModel(BaseModel):
    """Input for a generic model"""

    # Other input for BOW's: Set[tuple]
    # Other input for plainText: Set[str] (if we wan't to test one string outide of DB)

    input_data: Dict = Field(...)
    function_call: str = Field(...)


class GenericOutputModel(BaseModel):
    """Output for a generic model"""

    output_data: Dict = Field(...)
