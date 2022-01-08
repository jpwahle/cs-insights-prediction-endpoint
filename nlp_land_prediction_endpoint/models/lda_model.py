"""This module implements the LDA-Model"""
from typing import Any, Optional

from gensim.models.ldamodel import LdaModel  # type: ignore
from gensim.test.utils import common_corpus  # type: ignore

from nlp_land_prediction_endpoint.models.generic_model import (
    GenericModel as myGeneric_Model,
)


class LDA_Model(myGeneric_Model):
    """Implementation of the LDA (Latent Dirichlet Allocation Model)"""

    def __init__(self, **data: Any) -> None:
        """Create LDA_Model"""
        data["name"] = "LDA"
        data["description"] = "Latent Dirichlet allocation model"
        # XXX-TN    Maybe we should consider adding another model
        #           for the creationParameters, so we can validate the input
        if "creationParameters" in data:
            data["processingModel"] = LdaModel(**data["creationParameters"])
        else:
            data["processingModel"] = LdaModel(common_corpus, num_topics=10)
        data["inputObject"] = {
            # just docs (M) are mandatory, others can be computed
            "numOfTopics": Optional[int],  # aka k, default = 100
            "topics": Optional[dict],  # aka K
            "numOfVocs": Optional[int],  # num of words in vocabulary, aka v
            "vocabulary": set,  # words in vocabulary, aka V #do as set?
            "numOfDocs": Optional[int],  # num of documents, aka m
            "docs": set,  # documents id as str -> convert in set (hashed) of str #do as set?
        }
        super().__init__(**data)

    def alpha(self, document: str) -> dict:
        """Calc alpha and return"""
        topic = {
            "name": "AI",
            "keyword": "Deep Learning; Knowledge; Computer Vison",
            "weight": 0.123,
        }
        return topic

    def beta(self, topic: str, word: str) -> dict:
        """Calc beta and return it"""
        probability = {
            "word": "consetetur",
            "probability": "0.0312",
        }

        return probability

    def phi(self, word: str, topic: str) -> float:
        """Calc probability of word w occurring in topic k"""
        probability = 0.213
        return probability

    def theta(self, topic: str, document: str) -> float:
        """Calc probability of topic k occurring in document d"""
        probability = 0.223
        return probability

    def getk(self) -> Any:
        """Returns and computes k (Number of topics)

        Returns:
            Any: number of topics
        """
        return len(self.getK())

    def getNumTopics(self) -> Any:
        """Returns and computes Number of topics

        Returns:
            Any: number of topics
        """
        return self.getk()

    def getK(self) -> Any:
        """Returns and computes K (Topics in a dict)

        Returns:
            Any: A dictionary containing the topics
        """
        return self.processingModel.get_topics().tolist()

    def getTopics(self) -> Any:
        """Returns and computes K (Topics in a dict)

        Returns:
            Any: A dictionary containing the topics
        """
        return self.getK()
