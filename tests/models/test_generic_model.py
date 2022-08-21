"""Tests for the generic model."""
from datetime import datetime

import pytest

from cs_insights_prediction_endpoint.models.generic_model import GenericModel


@pytest.fixture
def dummy_generic_model() -> GenericModel:
    """Provides an actual instance of the implementaion

    Returns:
        GenericModel: the created GenericModel
    """
    dummy_values = {
        "name": "Generic",
        "created_by": "Alpha Tester",
        "description": "This is a test",
        "creation_parameters": {},
        "function_calls": {},
        "type_of_model": "test",
    }
    dummy = GenericModel(**dummy_values)
    return dummy


def test_generic_model_initial_values(dummy_generic_model: GenericModel) -> None:
    """Test for checking if the Generic_Model gets created correctly

    Arguments:
        dummy_generic_model (Generic_Model): An instance of our GenericModel implementation
    """
    assert dummy_generic_model.name == "Generic"
    assert str(hash(dummy_generic_model.name)) == dummy_generic_model.id
    assert dummy_generic_model.get_name() == dummy_generic_model.name
    assert dummy_generic_model.created_by == "Alpha Tester"
    assert dummy_generic_model.created_at <= datetime.timestamp(datetime.now()) + 1
    assert dummy_generic_model.created_at >= datetime.timestamp(datetime.now()) - 1
    assert dummy_generic_model.description == "This is a test"
    assert dummy_generic_model.creation_parameters == {}
    assert dummy_generic_model.function_calls == {}
    assert dummy_generic_model.get_function_calls() == []
    assert str(dummy_generic_model) == dummy_generic_model.id

    with pytest.raises(NotImplementedError):
        dummy_generic_model.train({})

    with pytest.raises(NotImplementedError):
        dummy_generic_model.predict({})

    with pytest.raises(NotImplementedError):
        dummy_generic_model.save("")

    with pytest.raises(NotImplementedError):
        dummy_generic_model.load("")
