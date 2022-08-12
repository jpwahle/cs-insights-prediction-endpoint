"""This modulew implements the generic-model"""
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T", bound="GenericModel")


class GenericModel(BaseModel):
    """Generic Model."""

    id: str
    name: str = Field(..., min_length=1, max_length=32)
    createdBy: str = Field(...)
    createdAt: float
    description: str = Field(...)
    # XXX-TN We should a GenericCreationParameters, same as GenericInputModel
    creationParameters: Optional[dict] = {}
    saveDirectory: Optional[str] = "./saved_models"
    type: str = Field(...)

    functionCalls: dict = Field(...)

    processingModel: Any

    def __init__(self: T, **data: Any) -> None:
        """Constructor for GenericModel"""
        data["createdAt"] = datetime.timestamp(datetime.now())
        data["id"] = "Model-" + data["name"] + "-" + str(data["createdAt"] * random.random())
        Path(saveDirectory).mkdir(parents=True, exist_ok=True)
        super().__init__(**data)

        Path(self.saveDirectory).mkdir(parents=True, exist_ok=True)

    def __str__(self: T) -> str:
        """Returns the String-representation of this GenericModel instance

        Returns:
            str: String representation of this GenericModel instance
        """
        return self.id

    def getId(self: T) -> str:
        """Returns the id of the object

        Returns:
            str: The id of the current object
        """
        return self.id

    def getName(self: T) -> str:
        """Returns the name of the object

        Returns:
            str: The name of the current object
        """
        return self.name

    def getFunctionCalls(self: T) -> list:
        """Returns the name of all the functions available

        Returns:
            list: Names of all implemented functions
        """
        return list(self.functionCalls.keys())

    def train(self: T, inputObject: dict) -> None:
        """Train the model with data from inputObject"""
        raise NotImplementedError("GenericModel.train has to be implemented by the subclass")

    def predict(self: T, inputObject: dict) -> list:
        """Predict something with data from inputObject"""
        raise NotImplementedError("GenericModel.predict has to be implemented by the subclass")

    def save(self: T, path: str) -> None:
        """Function to save the state of the model"""
        pass

    def load(self: T, path: str) -> None:
        """Function to load the state of the model"""
        pass


class GenericInputModel(BaseModel):
    """Input for a generic model"""

    # Other input for BOW's: Set[tuple]
    # Other input for plainText: Set[str] (if we wan't to test one string outide of DB)

    inputData: Dict = Field(...)
    functionCall: str = Field(...)


class GenericOutputModel(BaseModel):
    """Output for a generic model"""

    outputData: Dict = Field(...)
