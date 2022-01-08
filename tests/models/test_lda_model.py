"""Test the lda model."""
import sys
from datetime import datetime
from typing import Optional

import pytest
from gensim.models.ldamodel import LdaModel
from gensim.test.utils import common_corpus

from nlp_land_prediction_endpoint.models.lda_model import LDA_Model


@pytest.fixture
def dummy_lda_instance() -> LdaModel:
    return LdaModel(common_corpus, num_topics=10)


@pytest.fixture
def dummy_lda_model() -> LDA_Model:
    dummy_values = {
        "createdBy": "Alpha Tester",
        "creationParameters": {},
        "outputObject": {},
        "functionCalls": {},
    }
    dummy = LDA_Model(**dummy_values)
    return dummy


def test_lda_model_initial_values(dummy_lda_model: LDA_Model, dummy_lda_instance: LdaModel) -> None:
    print("Real: ", dummy_lda_model.getTopics())
    print("Test: ", dummy_lda_instance.get_topics().tolist())
    assert dummy_lda_model.name == "LDA"
    assert "Model" + dummy_lda_model.name in dummy_lda_model.id
    assert "Model" + dummy_lda_model.name in dummy_lda_model.getId()
    assert dummy_lda_model.createdBy == "Alpha Tester"
    assert dummy_lda_model.createdAt <= datetime.timestamp(datetime.now()) + 1
    assert dummy_lda_model.createdAt >= datetime.timestamp(datetime.now()) - 1
    assert dummy_lda_model.description == "Latent Dirichlet allocation model"
    assert dummy_lda_model.creationParameters == {}
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
    assert sys.getsizeof(dummy_lda_model.getK()) == sys.getsizeof(
        dummy_lda_instance.get_topics().tolist()
    )

    assert len(dummy_lda_model.getTopics()) == len(dummy_lda_instance.get_topics().tolist())
