"""Test the storage controller."""

import mongomock
import pytest

from cs_insights_prediction_endpoint.models.generic_model import GenericModel
from cs_insights_prediction_endpoint.utils.settings import get_settings
from cs_insights_prediction_endpoint.utils.storage_controller import StorageController


@pytest.fixture
def dummyGenericModel() -> GenericModel:
    """Provides a dummy model

    Returns:
        GenericModel: empty
    """
    dummy_values = {
        "name": "Generic",
        "createdBy": "Alpha Tester",
        "description": "This is a test",
        "creationParameters": {},
        "functionCalls": {},
        "type": "lda",
    }
    dummy = GenericModel(**dummy_values)

    return dummy


@pytest.fixture
def dummyStorageController(dummyGenericModel: GenericModel) -> StorageController:
    """Provides a dummy storage controller

    Returns:
        StorageController: empty
    """
    mongomock.patch(servers=(("127.0.0.1", 27017),))
    return StorageController(get_settings())


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def testDeleteModel(dummyGenericModel: GenericModel) -> None:
    """Test for deleteing models from the StorageController

    Arguments:
        dummyStorageController (StorageController): A dummy storage_controller
        dummyGenericModel (GenericModel): A dummy GenericModel
    """
    dummyStorageController = StorageController(get_settings())
    # add
    dummyStorageController.addModel(dummyGenericModel)
    # delete
    dummyStorageController.delModel(dummyGenericModel.id)
    assert dummyStorageController.getModel(dummyGenericModel.id) is None

    # Try to delete no existent Model
    with pytest.raises(KeyError):
        dummyStorageController.delModel("kjsdhgf8iuz")


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def testAddModel(dummyGenericModel: GenericModel) -> None:
    """Test for adding models to the StorageController

    Arguments:
        dummyStorageController (StorageController): A dummy storage_controller
        dummyGenericModel (GenericModel): A dummy GenericModel
    """
    dummyStorageController = StorageController(get_settings())
    old = dummyStorageController.getAllModels()
    dummyStorageController.addModel(dummyGenericModel)

    assert dummyStorageController.getAllModels() == old
    assert dummyStorageController.getModel(dummyGenericModel.id) == dummyGenericModel
    restartedStorageController = StorageController(get_settings())
    assert len(restartedStorageController.getAllModels()) > 0
