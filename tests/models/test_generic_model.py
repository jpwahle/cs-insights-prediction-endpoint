"""Tests for the generic model."""
from datetime import datetime

import pytest

from nlp_land_prediction_endpoint.models.generic_model import GenericModel


@pytest.fixture
def dummy_generic_model() -> GenericModel:
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


def test_generic_model_initial_values(dummy_generic_model: GenericModel) -> None:
    assert dummy_generic_model.name == "Generic"
    assert "Model" + dummy_generic_model.name in dummy_generic_model.id
    assert "Model" + dummy_generic_model.getName() in dummy_generic_model.getId()
    assert dummy_generic_model.createdBy == "Alpha Tester"
    assert dummy_generic_model.createdAt <= datetime.timestamp(datetime.now()) + 1
    assert dummy_generic_model.createdAt >= datetime.timestamp(datetime.now()) - 1
    assert dummy_generic_model.description == "This is a test"
    assert dummy_generic_model.creationParameters == {}
    assert dummy_generic_model.inputObject == {}
    assert dummy_generic_model.outputObject == {}
    assert dummy_generic_model.functionCalls == {}

    with pytest.raises(Exception) as execinfo:
        dummy_generic_model.train({})
        assert execinfo.value.args[0] == "NotImplemented"

    with pytest.raises(Exception) as execinfo:
        dummy_generic_model.predict({})
        assert execinfo.value.args[0] == "NotImplemented"
