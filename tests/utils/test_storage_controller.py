"""Test the storage controller."""

import mongomock
import pytest

from cs_insights_prediction_endpoint.models.generic_model import generic_model
from cs_insights_prediction_endpoint.utils.settings import get_settings
from cs_insights_prediction_endpoint.utils.storage_controller import storage_controller


@pytest.fixture
def dummygeneric_model() -> generic_model:
    """Provides a dummy model

    Returns:
        generic_model: empty
    """
    dummy_values = {
        "name": "Generic",
        "created_by": "Alpha Tester",
        "description": "This is a test",
        "creation_parameters": {},
        "function_calls": {},
        "type": "lda",
    }
    dummy = generic_model(**dummy_values)

    return dummy


@pytest.fixture
def dummystorage_controller(dummygeneric_model: generic_model) -> storage_controller:
    """Provides a dummy storage controller

    Returns:
        storage_controller: empty
    """
    mongomock.patch(servers=(("127.0.0.1", 27017),))
    return storage_controller(get_settings())


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def testDeleteModel(dummygeneric_model: generic_model) -> None:
    """Test for deleteing models from the storage_controller

    Arguments:
        dummystorage_controller (storage_controller): A dummy storage_controller
        dummygeneric_model (generic_model): A dummy generic_model
    """
    dummystorage_controller = storage_controller(get_settings())
    # add
    dummystorage_controller.add_model(dummygeneric_model)
    # delete
    dummystorage_controller.del_model(dummygeneric_model.id)
    assert dummystorage_controller.get_model(dummygeneric_model.id) is None

    # Try to delete no existent Model
    with pytest.raises(KeyError):
        dummystorage_controller.del_model("kjsdhgf8iuz")


@mongomock.patch(servers=(("127.0.0.1", 27017),))
def testAddModel(dummygeneric_model: generic_model) -> None:
    """Test for adding models to the storage_controller

    Arguments:
        dummystorage_controller (storage_controller): A dummy storage_controller
        dummygeneric_model (generic_model): A dummy generic_model
    """
    dummystorage_controller = storage_controller(get_settings())
    old = dummystorage_controller.get_all_models()
    dummystorage_controller.add_model(dummygeneric_model)

    assert dummystorage_controller.get_all_models() == old
    assert dummystorage_controller.get_model(dummygeneric_model.id) == dummygeneric_model
    restartedstorage_controller = storage_controller(get_settings())
    assert len(restartedstorage_controller.get_all_models()) > 0
    added_model = restartedstorage_controller.get_model(dummygeneric_model.get_id())
    assert added_model is not None
    assert added_model.name == dummygeneric_model.name
