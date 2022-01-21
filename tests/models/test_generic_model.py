"""Tests for the generic model."""
from datetime import datetime

import pytest

from nlp_land_prediction_endpoint.models.generic_model import GenericModel


@pytest.fixture
def dummy_generic_model() -> GenericModel:
    """Provides an actual instance of the implementaion

    Returns:
        GenericModel: the created GenericModel
    """
    dummy_values = {
        "name": "Generic",
        "createdBy": "Alpha Tester",
        "description": "This is a test",
        "creationParameters": {},
        "functionCalls": {},
    }
    dummy = GenericModel(**dummy_values)
    return dummy


def test_generic_model_initial_values(dummy_generic_model: GenericModel) -> None:
    """Test for checking if the Generic_Model gets created correctly

    Arguments:
        dummy_generic_model (Generic_Model): An instance of our GenericModel implementation
    """
    assert dummy_generic_model.name == "Generic"
    assert "Model" + dummy_generic_model.name in dummy_generic_model.id
    assert "Model" + dummy_generic_model.getName() in dummy_generic_model.getId()
    assert dummy_generic_model.createdBy == "Alpha Tester"
    assert dummy_generic_model.createdAt <= datetime.timestamp(datetime.now()) + 1
    assert dummy_generic_model.createdAt >= datetime.timestamp(datetime.now()) - 1
    assert dummy_generic_model.description == "This is a test"
    assert dummy_generic_model.creationParameters == {}
    assert dummy_generic_model.functionCalls == {}
    assert dummy_generic_model.getFunctionCalls() == []
    assert str(dummy_generic_model) == dummy_generic_model.id

    with pytest.raises(NotImplementedError):
        dummy_generic_model.train({})

    with pytest.raises(NotImplementedError):
        dummy_generic_model.predict({})
