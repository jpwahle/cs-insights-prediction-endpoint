"""This module implements a storage controller for the endpoint management"""

from typing import Optional, Set
from nlp_land_prediction_endpoint.models.generic_model import GenericModel


class StorageController:
    models: Set[GenericModel] = Set()

    def getModel(self, id: str) -> Optional[GenericModel]:
        """Returns the model with id"""
        for model in self.models:
            if model.id == id:
                return model
        return None

    def getAllModels(self) -> Set[GenericModel]:
        """Returns all models"""
        return self.models

    def addModel(self, model: GenericModel) -> str:
        """Adds model to models"""
        self.models.add(model)
        return model.id

    def delModel(self, id: str) -> None:
        """Delete model from storage"""
        model = self.getModel(id)
        if model is None:
            raise KeyError("Model not found")
        else:
            self.models.remove(model)
