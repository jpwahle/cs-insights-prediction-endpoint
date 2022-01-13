"""Test the lda model."""
from datetime import datetime
from typing import Optional
from nlp_land_prediction_endpoint.models.generic_model import GenericModel

import pytest
from gensim.models.ldamodel import LdaModel
from gensim.test.utils import common_corpus

from nlp_land_prediction_endpoint.utils.storage_controller import StorageController


@pytest.fixture
def dummyStorageController() -> StorageController:
    """Provides a dummy storage controller

    Returns:
        StorageController: empty
    """
    dummy = StorageController()
    return dummy


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
        "inputObject": {},
        "outputObject": {},
        "functionCalls": {},
    }
    dummy = GenericModel(**dummy_values)

    return dummy


def testAddModel(
    dummyStorageController: StorageController, dummyGenericModel: GenericModel
) -> None:
    dummyStorageController.addModel(dummyGenericModel)

    assert dummyStorageController.getAllModels() == set(dummyGenericModel)
    assert dummyStorageController.getModel(dummyGenericModel.id) == dummyGenericModel


def testDeleteModel(
    dummyStorageController: StorageController, dummyGenericModel: GenericModel
) -> None:
    # add
    dummyStorageController.addModel(dummyGenericModel)
    # delete
    dummyStorageController.delModel(dummyGenericModel.id)

    assert dummyStorageController.getAllModels() == set()
    assert dummyStorageController.getModel(dummyGenericModel.id) is None

    with pytest.raises(KeyError):
        dummyStorageController.delModel("kjsdhgf8iuz")
