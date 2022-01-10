"""This modulew implements the generic-model"""
import random
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class GenericModel(BaseModel):
    """Generic Model."""

    id: str
    name: str = Field(..., min_length=1, max_length=32)
    createdBy: str = Field(...)
    createdAt: float
    description: str = Field(...)
    creationParameters: Optional[dict]

    # XXX-TN Maybe we should also create Models for the following two dicts.
    #        This will make it easier to catch errors as well as provbide some nice
    #        structure to the project.
    #        It could be as follows:
    #           - GenericModelInput
    #               - SomeModelImplementaionInput(GenericModelInput)
    #               - SomeOtherModelInput(GenericModelInput)
    #        Where GenericModelInput could contain keys like "paperIds", "corpus", "bow".
    #        And SomeModelImplementaionInput would contain model specific keys
    #        like "number of rounds".
    #        The same applies to outputObject
    inputObject: dict
    outputObject: dict
    functionCalls: dict = Field(...)

    processingModel: Any

    def __init__(self, **data: Any) -> None:
        """Test"""
        data["createdAt"] = datetime.timestamp(datetime.now())
        data["id"] = "Model" + data["name"] + str(data["createdAt"] * random.random())
        super().__init__(**data)

    def getId(self) -> str:
        """Returns the id of the object

        Returns:
            str: The id of the current object
        """
        return self.id

    def getName(self) -> str:
        """Returns the name of the object

        Returns:
            str: The name of the current object
        """
        return self.name

    def getFunctionCalls(self) -> list:
        """Returns the name of all the functions available

        Returns:
            list: Names of all implemented functions
        """
        return list(self.functionCalls.keys())

    def train(self, inputObject: dict) -> None:
        """Train the model with data from inputObject"""
        raise NotImplementedError("GenericModel.train has to be implemented by the subclass")

    def predict(self, inputObject: dict) -> list:
        """Predict something with data from inputObject"""
        raise NotImplementedError("GenericModel.predict has to be implemented by the subclass")
