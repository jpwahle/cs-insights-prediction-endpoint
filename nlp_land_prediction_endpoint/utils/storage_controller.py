"""This module implements a storage controller for the endpoint management"""

from typing import Optional, Set, TypeVar

from nlp_land_prediction_endpoint.models.generic_model import GenericModel

T = TypeVar("T", bound="StorageController")


# XXX-TN This will be only a temporary implementation
#        we should create an Issue for an actual implementation
class StorageController:
    """Storage Controller class to enable access to currently created Models"""

    models: Set[GenericModel] = set([])

    def __init__(self: T) -> None:
        """Constructor for the storage controller"""
        self.models = set([])

    def getModel(self: T, id: str) -> Optional[GenericModel]:
        """Returns the model with id"""
        for model in self.models:
            if model.id == id:
                return model
        return None

    def getAllModels(self: T) -> Set[GenericModel]:
        """Returns all models"""
        return self.models

    def addModel(self: T, model: GenericModel) -> str:
        """Adds model to models"""
        self.models.add(model)
        return model.id

    def delModel(self: T, id: str) -> None:
        """Delete model from storage"""
        model = self.getModel(id)
        if model is None:
            raise KeyError("Model not found")
        else:
            self.models.remove(model)


storage: StorageController = StorageController()
