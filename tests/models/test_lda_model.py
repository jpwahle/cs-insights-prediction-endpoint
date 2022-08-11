"""Test the lda model."""
from datetime import datetime

import pytest
from gensim.models.ldamodel import LdaModel
from gensim.test.utils import common_corpus

from cs_insights_prediction_endpoint.models.lda_model import LDAModel


@pytest.fixture
def dummy_creation_parameters() -> dict:
    """Provides some creation parameters to LDAModel as well as
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
def dummy_lda_model(dummy_creation_parameters: dict) -> LDAModel:
    """Provides an actual instance of the implementaion

    Arguments:
        dummy_creation_parameters (dict): the creation parameters for the lda model

    Returns:
        LDAModel: The created LDAModel
    """
    dummy_values = {
        "createdBy": "Alpha Tester",
        "creationParameters": dummy_creation_parameters,
        "functionCalls": {},
        "type": "lda",
    }
    dummy = LDAModel(**dummy_values)
    return dummy


@pytest.fixture
def dummy_lda_model_no_creation_parameters() -> LDAModel:
    """Provides an actual instance of the implementaion but without any creation parameters

    Returns:
        LDAModel: tthe created LDAModel
    """
    dummy_values = {
        "createdBy": "Alpha Tester",
        "functionCalls": {},
        "type": "lda",
    }
    dummy = LDAModel(**dummy_values)
    return dummy


def test_lda_model_initial_values(
    dummy_lda_model: LDAModel,
    dummy_lda_instance: LdaModel,
    dummy_creation_parameters: dict,
) -> None:
    """Test for checking if the LDAModel gets created correctly

    Arguments:
        dummy_lda_model (LDAModel): An instance of our LDA_Model implementation
        dummy_lda_instance (LdaModel): The Actual object from gensim used for assertions
        dummy_creation_parameters (dict): The dictionary containing the creation parameters
        of the LdaModel instance
    """
    assert dummy_lda_model.name == "LDA"
    assert "Model-" + dummy_lda_model.name in dummy_lda_model.id
    assert "Model-" + dummy_lda_model.name in dummy_lda_model.getId()
    assert dummy_lda_model.createdBy == "Alpha Tester"
    assert dummy_lda_model.createdAt <= datetime.timestamp(datetime.now()) + 1
    assert dummy_lda_model.createdAt >= datetime.timestamp(datetime.now()) - 1
    assert dummy_lda_model.description == "Latent Dirichlet allocation model"
    assert dummy_lda_model.creationParameters == dummy_creation_parameters
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

    dummy_lda_instance.update(common_corpus)
    dummy_lda_model.train({"corpus": common_corpus})
    assert dummy_lda_model.getTopics() == dummy_lda_instance.get_topics().tolist()
    test_training = list(dummy_lda_instance.get_document_topics(common_corpus))
    assert dummy_lda_model.predict({"bow": common_corpus}) == test_training

    assert (
        isinstance(
            dummy_lda_model.getLDAvis(
                [
                    {"title": "Test1", "abstractText": "Test1"},
                    {"title": "Test2", "abstractText": "Test2"},
                    {"title": "Test3", "abstractText": "Test3"},
                ],
                num_topics=3,
                passes=1,
            ),
            dict,
        )
        is True
    )


def test_lda_model_initial_values_no_creation_paramers(
    dummy_lda_model_no_creation_parameters: LDAModel, dummy_lda_instance: LdaModel
) -> None:
    """Test for checking if the LDAModel gets created correctly (without creation parameters)

    Arguments:
        dummy_lda_model_no_creation_parameters (LDAModel): An instance of our
        LDA_Model implementation
        dummy_lda_instance (LdaModel): The Actual object from gensim used for assertions
    """
    assert dummy_lda_model_no_creation_parameters.name == "LDA"
    assert (
        "Model-" + dummy_lda_model_no_creation_parameters.name
        in dummy_lda_model_no_creation_parameters.id
    )
    assert (
        "Model-" + dummy_lda_model_no_creation_parameters.name
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
    assert dummy_lda_model_no_creation_parameters.creationParameters == {}
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
    # We cannot assert getTopics like we did in the previous test due to randomness in LDA
    assert len(dummy_lda_model_no_creation_parameters.getK()) == len(
        dummy_lda_instance.get_topics().tolist()
    )
    assert len(dummy_lda_model_no_creation_parameters.getTopics()) == len(
        dummy_lda_instance.get_topics().tolist()
    )
