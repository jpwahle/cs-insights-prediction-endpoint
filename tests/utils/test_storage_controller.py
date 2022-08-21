"""Test the storage controller."""

import mongomock
import pytest

from cs_insights_prediction_endpoint.models.generic_model import GenericModel
from cs_insights_prediction_endpoint.utils.settings import get_settings
from cs_insights_prediction_endpoint.utils.storage_controller import StorageController


@pytest.fixture
def dummy_generic_model() -> GenericModel:
    """Provides a dummy model

    Returns:
        GenericModel: empty
    """
    dummy_values = {
        "name": "Generic",
        "created_by": "Alpha Tester",
        "description": "This is a test",
        "creation_parameters": {},
        "function_calls": {},
        "type_of_model": "lda",
    }
    dummy = GenericModel(**dummy_values)

    return dummy


@pytest.fixture
def dummy_storage_controller(dummy_generic_model: GenericModel) -> StorageController:
    """Provides a dummy storage controller

    Returns:
        StorageController: empty
    """
    mongomock.patch(servers=(("127.0.0.1", 27017),))
    return StorageController(get_settings())


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_delete_model(dummy_generic_model: GenericModel) -> None:
    """Test for deleteing models from the StorageController

    Arguments:
        dummy_storage_controller (StorageController): A dummy storage_controller
        dummy_generic_model (GenericModel): A dummy GenericModel
    """
    dummy_storage_controller = StorageController(get_settings())
    # add
    dummy_storage_controller.add_model(dummy_generic_model)
    # delete
    dummy_storage_controller.del_model(dummy_generic_model.id)
    assert dummy_storage_controller.get_model(dummy_generic_model.id) is None

    # Try to delete no existent Model
    with pytest.raises(KeyError):
        dummy_storage_controller.del_model("kjsdhgf8iuz")


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def test_add_model(dummy_generic_model: GenericModel) -> None:
    """Test for adding models to the StorageController

    Arguments:
        dummy_storage_controller (StorageController): A dummy storage_controller
        dummy_generic_model (GenericModel): A dummy GenericModel
    """
    dummy_storage_controller = StorageController(get_settings())
    old = dummy_storage_controller.get_all_models()
    dummy_storage_controller.add_model(dummy_generic_model)

    assert dummy_storage_controller.get_all_models() == old
    assert dummy_storage_controller.get_model(dummy_generic_model.id) == dummy_generic_model
    restarted_storage_controller = StorageController(get_settings())
    assert len(restarted_storage_controller.get_all_models()) > 0
    added_model = restarted_storage_controller.get_model(dummy_generic_model.get_id())
    assert added_model is not None
    assert added_model.name == dummy_generic_model.name
