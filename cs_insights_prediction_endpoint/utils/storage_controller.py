"""This module implements a storage controller for the endpoint management"""

from functools import lru_cache
from importlib import import_module
from typing import Any, List, Optional, TypeVar

import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection

from cs_insights_prediction_endpoint.models.generic_model import generic_model
from cs_insights_prediction_endpoint.utils.settings import Settings, get_settings

T = TypeVar("T", bound="storage_controller")

# Attributes to exclude when saving pydentic models to the database
exclude_attributes: Any = {"function_calls": True, "processing_model": True}


class storage_controller:
    """Storage Controller class to enable access to currently created Models"""

    models: List[generic_model] = list([])

    def __init__(self: T, settings: Settings) -> None:
        """Constructor for the storage controller
        Args:
            settings (Settings): Settings object used for information on the databse
        """
        self.model_client: MongoClient = pymongo.MongoClient(
            f"mongodb://{settings.mongo_user.get_secret_value()}"
            + f":{settings.mongo_password.get_secret_value()}@{settings.mongo_host}",
        )
        self.model_db: Collection = self.model_client[settings.model_db_name][
            settings.model_db_name
        ]
        self.models = list([])

        for db_model in self.model_db.find({}):
            # self.models.append(GenericModel(**model))
            for implemented_models in settings.implemented_models:
                if db_model["type_of_model"] in implemented_models:
                    model_specs = implemented_models[db_model["type_of_model"]]
                    model_module = import_module(model_specs[0])
                    model_class = model_specs[1]
                    model = getattr(model_module, model_class)(**db_model)
                    model.load(f"{model.save_directory}/{model.id}")
                    self.models.append(model)

    def get_model(self: T, id: str) -> Optional[GenericModel]:
        """Returns the model with id"""
        for model in self.models:
            if model.id == id:
                return model
        return None

    def get_all_models(self: T) -> List[GenericModel]:
        """Returns all models"""
        return self.models

    def add_model(self: T, model: GenericModel) -> str:
        """Adds model to models"""
        self.model_db.insert_one(model.dict(exclude=exclude_attributes))
        self.models.append(model)
        return model.id

    # TODO For consitency maybe return bool or switch
    #      remote_storage_controler function to raise key error
    def del_model(self: T, id: str) -> None:
        """Delete model from storage"""
        model = self.get_model(id)
        if model is None:
            raise KeyError("Model not found")
        else:
            self.model_db.delete_one({"id": model.id})
            self.models.remove(model)


# storage_controller: storage_controller = storage_controller(get_settings())


@lru_cache()
def get_storage_controller() -> storage_controller:
    """Return the storage_controller instance"""
    return storage_controller(get_settings())
    # return storage_controller
