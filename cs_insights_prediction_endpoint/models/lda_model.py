"""This module implements the LDA-Model"""
import json
from datetime import datetime
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

from cs_insights_prediction_endpoint.models.generic_model import (
    GenericInputModel,
    GenericModel,
    GenericOutputModel,
)

T = TypeVar("T", bound="LdaModelWrapper")


class LdaModelWrapper(GenericModel):
    """Implementation of the LDA (Latent Dirichlet Allocation Model)"""

    def __init__(self: T, **data: Any) -> None:
        """Create LdaModelWrapper"""
        if "name" not in data:
            data["name"] = "Unnamed-LDA-" + str(hash(datetime.timestamp(datetime.now())))
        # XXX-TN We should consider adding "description" as a class config example
        if "description" not in data:
            data["description"] = "Latent Dirichlet allocation model"
        if "creation_parameters" in data and data["creation_parameters"] != {}:
            data["processing_model"] = LdaModel(**data["creation_parameters"])
        else:
            data["processing_model"] = LdaModel(common_corpus, num_topics=10)
        data["function_calls"] = {
            "alpha": self.alpha,
            "beta": self.beta,
            "phi": self.phi,
            "theta": self.theta,
            "getk": self.get_k,
            "getNumTopics": self.get_num_topics,
            "getK": self.get_topics_in_dict,
            "getTopics": self.get_topics,
            "getLDAvis": self.get_lda_vis,
            "train": self.train,
            "predict": self.predict,
        }
        super().__init__(**data)
        self.save(f"{self.save_directory}/{self.id}")

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

    def get_k(self: T) -> int:
        """Returns and computes k (Number of topics)

        Returns:
            Any: number of topics
        """
        return len(self.get_topics_in_dict())

    def get_num_topics(self: T) -> int:
        """Returns and computes Number of topics

        Returns:
            Any: number of topics
        """
        return self.get_k()

    def get_topics_in_dict(self: T) -> Any:
        """Returns and computes K (Topics in a dict)

        Returns:
            Any: A dictionary containing the topics
        """
        return self.processing_model.get_topics().tolist()

    def get_topics(self: T) -> Any:
        """Returns and computes K (Topics in a dict)

        Returns:
            Any: A dictionary containing the topics
        """
        return self.get_topics_in_dict()

    def get_lda_vis(
        self: T,
        data: List[Dict[str, str]],
        num_topics: int = 10,
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

        self.processing_model = LdaModel(
            bow_corpus, num_topics=num_topics, passes=passes, random_state=random_state
        )

        vis = pyLDAvis.gensim_models.prepare(self.processing_model, bow_corpus, dictionary, mds='mmds')

        return json.loads(vis.to_json())

    def train(self: T, input_object: dict) -> None:
        """Trains the LDAModel given a inputObject.
        The input object should at least contain some paper ids,
        which will be requested from the backend

        Arguments:
            input_object (dict): An inputObject where
            at least one key should contain data to process
        """
        # XXX-TN For now we will use corpus as input, which will be a proccessed bag of words.
        #        Later on this will be an array of paper ids. Maybe create an Issue?
        self.processing_model.update(**input_object)

    def predict(self: T, input_object: dict) -> list:
        """Given some input_object the LDAModel will classfiy the input data
        according to the data it was trained on
        Arguments:
            input_object (dict): An inputObject where
            at least one key should contain data to process

        Returns:
            list: A list containg the classified topics [(int, float)]
            as well as probabilites for the topics
        """
        # XXX-TN For now we will use corpus as input, which will be a proccessed bag of words.
        #        Later on this will be an array of paper. ids Maybe create an Issue?
        return list(self.processing_model.get_document_topics(**input_object))

    def save(self: T, path: str) -> None:
        """Function for saving a model to a path"""
        self.processing_model.save(path)

    def load(self: T, path: str) -> None:
        """Function for loading a model from a path"""
        self.processing_model.load(path)


class LdaInputModel(GenericInputModel):
    """Input for a generic model"""

    number_of_topics: Optional[int]
    topics: Optional[dict]
    num_of_vocs: Optional[int]
    vocabulary: set
    num_of_docs: Optional[int]


class LdaOutputModel(GenericOutputModel):
    """Output for a generic model"""

    topic_frequency: List[Tuple[str, float]]
