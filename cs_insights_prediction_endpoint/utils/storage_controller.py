"""This module implements a storage controller for the endpoint management"""

from functools import lru_cache
from importlib import import_module
from typing import Any, List, Optional, TypeVar

import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection

from cs_insights_prediction_endpoint.models.generic_model import GenericModel
from cs_insights_prediction_endpoint.utils.settings import Settings, get_settings

T = TypeVar("T", bound="StorageController")

# Attributes to exclude when saving pydentic models to the database
exclude_attributes: Any = {"functionCalls": True, "processingModel": True}


class StorageController:
    """Storage Controller class to enable access to currently created Models"""

    models: List[GenericModel] = list([])

    def __init__(self: T, settings: Settings) -> None:
        """Constructor for the storage controller
        Args:
            settings (Settings): Settings object used for information on the databse
        """
        print(get_settings())
        self.model_client: MongoClient = pymongo.MongoClient(
            f"mongodb://{settings.mongo_user.get_secret_value()}"
            + f":{settings.mongo_password.get_secret_value()}@{settings.mongo_host}",
        )
        self.model_db: Collection = self.model_client[settings.model_db_name][
            settings.model_db_name
        ]
        self.models = list([])

        for db_model in self.model_db.find():
            # self.models.append(GenericModel(**model))
            for implemented_models in settings.implemented_models:
                if db_model["type"] in implemented_models:
                    model_specs = implemented_models[db_model["type"]]
                    model_module = import_module(model_specs[0])
                    model_class = model_specs[1]
                    model = getattr(model_module, model_class)(**db_model)
                    model.load(f"{model.saveDirectory}/{model.id}")
                    self.models.append(model)

    def getModel(self: T, id: str) -> Optional[GenericModel]:
        """Returns the model with id"""
        for model in self.models:
            if model.id == id:
                return model
        return None

    def getAllModels(self: T) -> List[GenericModel]:
        """Returns all models"""
        return self.models

    def addModel(self: T, model: GenericModel) -> str:
        """Adds model to models"""
        self.model_db.insert_one(model.dict(exclude=exclude_attributes))
        self.models.append(model)
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


# storage_controller: StorageController = StorageController(get_settings())


@lru_cache()
def get_storage_controller() -> StorageController:
    """Return the storage_controller instance"""
    return StorageController(get_settings())
    # return storage_controller
