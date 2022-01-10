"""Test the lda model."""
from datetime import datetime
from typing import Optional

import pytest
from gensim.models.ldamodel import LdaModel
from gensim.test.utils import common_corpus

from nlp_land_prediction_endpoint.models.lda_model import LDA_Model


@pytest.fixture
def dummy_creation_parameters() -> dict:
    """Provides some creation parameters to LDA_Model as well as
    LdaModel (the instance to test against)
    Currently these three options are used:
        - corpus
        - num_topics
        - random_state

    Returns:
        dict: A dictionary containing the creation parameters
    """
    return {"corpus": common_corpus, "num_topics": 10, "random_state": 0}


@pytest.fixture
def dummy_lda_instance(dummy_creation_parameters: dict) -> LdaModel:
    """Provides the lda instance to test against

    Arguments:
        dummy_creation_parameters (dict): the creation parameters for the lda model

    Returns:
        LdaModel: the created LdaModel
    """
    return LdaModel(**dummy_creation_parameters)


@pytest.fixture
def dummy_lda_model(dummy_creation_parameters: dict) -> LDA_Model:
    """Provides an actual instance of the implementaion

    Arguments:
        dummy_creation_parameters (dict): the creation parameters for the lda model

    Returns:
        LDA_Model: tthe created LDA_Model
    """
    dummy_values = {
        "createdBy": "Alpha Tester",
        "creationParameters": dummy_creation_parameters,
        "outputObject": {},
        "functionCalls": {},
    }
    dummy = LDA_Model(**dummy_values)
    return dummy


@pytest.fixture
def dummy_lda_model_no_creation_parameters() -> LDA_Model:
    """Provides an actual instance of the implementaion but without any creation parameters

    Returns:
        LDA_Model: tthe created LDA_Model
    """
    dummy_values = {
        "createdBy": "Alpha Tester",
        "outputObject": {},
        "functionCalls": {},
    }
    dummy = LDA_Model(**dummy_values)
    return dummy


def test_lda_model_initial_values(
    dummy_lda_model: LDA_Model, dummy_lda_instance: LdaModel, dummy_creation_parameters: dict
) -> None:
    """Test for checking if the LDA_Model gets created correctly

    Arguments:
        dummy_lda_model (LDA_Model): An instance of our LDA_Model implementation
        dummy_lda_instance (LdaModel): The Actual object from gensim used for assertions
        dummy_creation_parameters (dict): The dictionary containing the creation parameters
        of the LdaModel instance
    """
    assert dummy_lda_model.name == "LDA"
    assert "Model" + dummy_lda_model.name in dummy_lda_model.id
    assert "Model" + dummy_lda_model.name in dummy_lda_model.getId()
    assert dummy_lda_model.createdBy == "Alpha Tester"
    assert dummy_lda_model.createdAt <= datetime.timestamp(datetime.now()) + 1
    assert dummy_lda_model.createdAt >= datetime.timestamp(datetime.now()) - 1
    assert dummy_lda_model.description == "Latent Dirichlet allocation model"
    assert dummy_lda_model.creationParameters == dummy_creation_parameters
    assert dummy_lda_model.inputObject == {
        "numOfTopics": Optional[int],  # aka k, default = 100
        "topics": Optional[dict],  # aka K
        "vocabulary": set,  # words in vocabulary, aka V #do as set?
        "numOfVocs": Optional[int],  # num of words in vocabulary, aka v
        "numOfDocs": Optional[int],  # num of documents, aka m
        "docs": set,  # documents id as str -> convert in set (hashed) of str #do as set?
    }
    assert dummy_lda_model.outputObject == {}
    assert dummy_lda_model.functionCalls == {}
    assert dummy_lda_model.alpha("None") == {
        "name": "AI",
        "keyword": "Deep Learning; Knowledge; Computer Vison",
        "weight": 0.123,
    }
    assert dummy_lda_model.beta("None", "None") == {
        "word": "consetetur",
        "probability": "0.0312",
    }
    assert dummy_lda_model.phi("None", "None") == 0.213
    assert dummy_lda_model.theta("None", "None") == 0.223

    assert dummy_lda_model.getk() == 10
    assert dummy_lda_model.getNumTopics() == 10
    # This assertion works, because we initialize it with the same random_state
    assert dummy_lda_model.getTopics() == dummy_lda_model.getK()
    assert dummy_lda_model.getTopics() == dummy_lda_instance.get_topics().tolist()

    assert len(dummy_lda_model.getTopics()) == len(dummy_lda_instance.get_topics().tolist())


def test_lda_model_initial_values_no_creation_paramers(
    dummy_lda_model_no_creation_parameters: LDA_Model, dummy_lda_instance: LdaModel
) -> None:
    assert dummy_lda_model_no_creation_parameters.name == "LDA"
    assert (
        "Model" + dummy_lda_model_no_creation_parameters.name
        in dummy_lda_model_no_creation_parameters.id
    )
    assert (
        "Model" + dummy_lda_model_no_creation_parameters.name
        in dummy_lda_model_no_creation_parameters.getId()
    )
    assert dummy_lda_model_no_creation_parameters.createdBy == "Alpha Tester"
    assert (
        dummy_lda_model_no_creation_parameters.createdAt <= datetime.timestamp(datetime.now()) + 1
    )
    assert (
        dummy_lda_model_no_creation_parameters.createdAt >= datetime.timestamp(datetime.now()) - 1
    )
    assert dummy_lda_model_no_creation_parameters.description == "Latent Dirichlet allocation model"
    assert dummy_lda_model_no_creation_parameters.creationParameters is None
    assert dummy_lda_model_no_creation_parameters.inputObject == {
        "numOfTopics": Optional[int],  # aka k, default = 100
        "topics": Optional[dict],  # aka K
        "vocabulary": set,  # words in vocabulary, aka V #do as set?
        "numOfVocs": Optional[int],  # num of words in vocabulary, aka v
        "numOfDocs": Optional[int],  # num of documents, aka m
        "docs": set,  # documents id as str -> convert in set (hashed) of str #do as set?
    }
    assert dummy_lda_model_no_creation_parameters.outputObject == {}
    assert dummy_lda_model_no_creation_parameters.functionCalls == {}
    assert dummy_lda_model_no_creation_parameters.alpha("None") == {
        "name": "AI",
        "keyword": "Deep Learning; Knowledge; Computer Vison",
        "weight": 0.123,
    }
    assert dummy_lda_model_no_creation_parameters.beta("None", "None") == {
        "word": "consetetur",
        "probability": "0.0312",
    }
    assert dummy_lda_model_no_creation_parameters.phi("None", "None") == 0.213
    assert dummy_lda_model_no_creation_parameters.theta("None", "None") == 0.223

    assert dummy_lda_model_no_creation_parameters.getk() == 10
    assert dummy_lda_model_no_creation_parameters.getNumTopics() == 10
    assert len(dummy_lda_model_no_creation_parameters.getK()) == len(
        dummy_lda_instance.get_topics().tolist()
    )
    assert len(dummy_lda_model_no_creation_parameters.getTopics()) == len(
        dummy_lda_instance.get_topics().tolist()
    )
