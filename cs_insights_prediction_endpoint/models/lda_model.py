"""This module implements the LDA-Model"""
import json
from typing import Any, Dict, List, Optional, Tuple, TypeVar

import pyLDAvis  # type: ignore
import pyLDAvis.gensim_models  # type: ignore
from gensim.corpora.dictionary import Dictionary  # type: ignore
from gensim.models.ldamodel import LdaModel  # type: ignore
from gensim.parsing.preprocessing import (  # type: ignore
    preprocess_string,
    remove_stopwords,
)
from gensim.test.utils import common_corpus  # type: ignore

from cs_insights_prediction_endpoint.models.generic_model import GenericInputModel
from cs_insights_prediction_endpoint.models.generic_model import (
    GenericModel as myGeneric_Model,
)
from cs_insights_prediction_endpoint.models.generic_model import GenericOutputModel

T = TypeVar("T", bound="LDAModel")


class LDAModel(myGeneric_Model):
    """Implementation of the LDA (Latent Dirichlet Allocation Model)"""

    def __init__(self: T, **data: Any) -> None:
        """Create LDAModel"""
        data["name"] = "LDA"
        # XXX-TN We should consider adding "description" as a class config example
        data["description"] = "Latent Dirichlet allocation model"
        # XXX-TN    Maybe we should consider adding another model
        #           for the creationParameters, so we can validate the input
        if "creationParameters" in data and data["creationParameters"] != {}:
            data["processingModel"] = LdaModel(**data["creationParameters"])
        else:
            data["processingModel"] = LdaModel(common_corpus, num_topics=10)
        data["functionCalls"] = {
            "alpha": self.alpha,
            "beta": self.beta,
            "phi": self.phi,
            "theta": self.theta,
            "getk": self.getk,
            "getNumTopics": self.getNumTopics,
            "getK": self.getK,
            "getTopics": self.getTopics,
            "getLDAvis": self.getLDAvis,
            "train": self.train,
            "predict": self.predict,
        }
        super().__init__(**data)
        self.save(f"{self.saveDirectory}/{self.id}")

    def alpha(self: T, document: str) -> dict:
        """Calc alpha and return"""
        topic = {
            "name": "AI",
            "keyword": "Deep Learning; Knowledge; Computer Vison",
            "weight": 0.123,
        }
        return topic

    def beta(self: T, topic: str, word: str) -> dict:
        """Calc beta and return it"""
        probability = {
            "word": "consetetur",
            "probability": "0.0312",
        }

        return probability

    def phi(self: T, word: str, topic: str) -> float:
        """Calc probability of word w occurring in topic k"""
        probability = 0.213
        return probability

    def theta(self: T, topic: str, document: str) -> float:
        """Calc probability of topic k occurring in document d"""
        probability = 0.223
        return probability

    def getk(self: T) -> int:
        """Returns and computes k (Number of topics)

        Returns:
            Any: number of topics
        """
        return len(self.getK())

    def getNumTopics(self: T) -> int:
        """Returns and computes Number of topics

        Returns:
            Any: number of topics
        """
        return self.getk()

    def getK(self: T) -> Any:
        """Returns and computes K (Topics in a dict)

        Returns:
            Any: A dictionary containing the topics
        """
        return self.processingModel.get_topics().tolist()

    def getTopics(self: T) -> Any:
        """Returns and computes K (Topics in a dict)

        Returns:
            Any: A dictionary containing the topics
        """
        return self.getK()

    def getLDAvis(
        self: T,
        data: List[Dict[str, str]],
        num_topics: int = 20,
        passes: int = 3,
        random_state: int = 0xBEEF,
    ) -> Any:
        """Returns the json output of the LDAvis library, which then gets processed by the frontend

        Args:
            data (Dict[str,str]): A dictionary containing the title and abstract texts of papers

        Returns:
            Dict[str, any]: The json output of the LDAvis library. Consider reading
                            https://pyldavis.readthedocs.io/en/latest/readme.html
        """
        docs = list([preprocess_string(remove_stopwords(i["title"])) for i in data])
        docs = docs + (
            list(
                [
                    preprocess_string(remove_stopwords(i["abstractText"]))
                    for i in data
                    if i["abstractText"] is not None
                ]
            )
        )

        dictionary = Dictionary(docs)
        bow_corpus = [dictionary.doc2bow(doc) for doc in docs]

        self.processingModel = LdaModel(
            bow_corpus, num_topics=num_topics, passes=passes, random_state=random_state
        )

        vis = pyLDAvis.gensim_models.prepare(self.processingModel, bow_corpus, dictionary)

        return json.loads(vis.to_json())

    def train(self: T, inputObject: dict) -> None:
        """Trains the LDAModel given a inputObject.
        The input object should at least contain some paper ids,
        which will be requested from the backend

        Arguments:
            inputObject (dict): An inputObject where
            at least one key should contain data to process
        """
        # XXX-TN For now we will use corpus as input, which will be a proccessed bag of words.
        #        Later on this will be an array of paper ids. Maybe create an Issue?
        self.processingModel.update(**inputObject)

    def predict(self: T, inputObject: dict) -> list:
        """Given some inputObject the LDAModel will classfiy the input data
        according to the data it was trained on
        Arguments:
            inputObject (dict): An inputObject where
            at least one key should contain data to process

        Returns:
            list: A list containg the classified topics [(int, float)]
            as well as probabilites for the topics
        """
        # XXX-TN For now we will use corpus as input, which will be a proccessed bag of words.
        #        Later on this will be an array of paper. ids Maybe create an Issue?
        return list(self.processingModel.get_document_topics(**inputObject))

    def save(self: T, path: str) -> None:
        """Function for saving a model to a path"""
        self.processingModel.save(path)

    def load(self: T, path: str) -> None:
        """Function for loading a model from a path"""
        self.processingModel.load(path)


class LDAInputModel(GenericInputModel):
    """Input for a generic model"""

    # just docs (M) are mandatory, others can be computed
    numOfTopics: Optional[int]  # aka k, default = 100
    topics: Optional[dict]  # aka K
    numOfVocs: Optional[int]  # num of words in vocabulary, aka v
    vocabulary: set  # words in vocabulary, aka V #do as set?
    numOfDocs: Optional[int]  # num of documents, aka m


class LDAOutputModel(GenericOutputModel):
    """Output for a generic model"""

    # wordID:float -> str: value
    # Ex.          -> attention: 0.4325

    topicFrequency: List[Tuple[str, float]]
