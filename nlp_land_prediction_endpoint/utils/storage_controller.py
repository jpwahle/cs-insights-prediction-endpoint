"""This module implements a storage controller for the endpoint management"""

from typing import Any, Optional, Set, TypeVar

from pymongo import MongoClient
from pymongo.collection import Collection

from nlp_land_prediction_endpoint.models.generic_model import GenericModel
from nlp_land_prediction_endpoint.utils.settings import Settings, get_settings

T = TypeVar("T", bound="StorageController")

# Attributes to exclude when saving pydentic models to the database
exclude_attributes: Any = {"functionCalls": True, "processingModel": True}


class StorageController:
    """Storage Controller class to enable access to currently created Models"""

    models: Set[GenericModel] = set([])

    def __init__(self: T, settings: Settings) -> None:
        """Constructor for the storage controller
        Args:
            settings (Settings): Settings object used for information on the databse
        """
        self.model_client: MongoClient = MongoClient(settings.MODEL_DB_URL)
        self.model_db: Collection = self.model_client[settings.MODEL_DB_NAME][
            settings.MODEL_DB_NAME
        ]
        self.models = set([])
        print(f"Successful connection to {settings.MODEL_DB_URL}")

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
        self.model_db.insert_one(model.dict(exclude=exclude_attributes))
        self.models.add(model)  # TODO check if actually added
        return model.id

    # TODO For consitency maybe return bool or switch
    #      remote_storage_controler function to raise key error
    def delModel(self: T, id: str) -> None:
        """Delete model from storage"""
        model = self.getModel(id)
        if model is None:
            raise KeyError("Model not found")
        else:
            self.model_db.delete_one({"id": model.id})  # TODO check if actually deleted
            self.models.remove(model)


storage_controller: StorageController = StorageController(get_settings())


def get_storage_controller() -> StorageController:
    """Return the storage_controller instance"""
    return storage_controller
