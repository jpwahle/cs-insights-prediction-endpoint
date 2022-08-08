"""This module implements a storage controller for the endpoint management"""

from typing import Optional, Set, TypeVar

from nlp_land_prediction_endpoint.models.generic_model import GenericModel
from nlp_land_prediction_endpoint.utils.settings import Settings, get_settings
import motor.motor_asyncio

T = TypeVar("T", bound="StorageController")


# XXX-TN This will be only a temporary implementation
#        we should create an Issue for an actual implementation
class StorageController:
    """Storage Controller class to enable access to currently created Models"""

    models: Set[GenericModel] = set([])
    model_client = None
    model_db = None

    def __init__(self: T) -> None:
        """Constructor for the storage controller"""
    def __init__(self: T, settings: Settings):
        self.model_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MODEL_DB_URL)
        self.model_db = self.model_client[settings.REMOTE_HOST_DB_NAME][settings.MODEL_DB_NAME]
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
        self.models.add(model)
        return model.id

    def delModel(self: T, id: str) -> None:
        """Delete model from storage"""
        model = self.getModel(id)
        if model is None:
            raise KeyError("Model not found")
        else:
            self.models.remove(model)


storage_controller: StorageController = StorageController(get_settings())
def get_storage_controller():
    return storage_controller
