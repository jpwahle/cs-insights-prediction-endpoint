"""This module implements the models for papers."""
from __future__ import annotations

from datetime import datetime
from typing import List

from bson.objectid import ObjectId  # type: ignore
from pydantic import AnyUrl, BaseModel, Field

from cs_insights_prediction_endpoint.enums.enum_paper import (
    ExtractionMethod,
    ShortLong,
    TypeOfPaper,
)


class PaperModel(BaseModel):
    """The model for a paper. Should be identical to the NLP-Land-backend.

    Args:
        BaseModel (Any): Base class of FastAPI models.
    """

    id: str = Field(...)
    title: str = Field(...)
    abstractText: str = Field(...)
    abstractExtractor: ExtractionMethod = Field(...)
    typeOfPaper: TypeOfPaper = Field(...)
    shortOrLong: ShortLong = Field(...)

    atMainConference: bool = Field(...)
    isSharedTask: bool = Field(...)
    isStudentPaper: bool = Field(...)

    doi: str = Field(...)
    preProcessingGitHash: str = Field(...)
    pdfUrl: AnyUrl = Field(...)
    absUrl: AnyUrl = Field(...)

    datePublished: str = Field(...)
    citationInfoTimestamp: str = Field(...)
    citedBy: List[str] = Field(...)

    authors: List[str] = Field(...)
    firstAuthor: str = Field(...)
    venues: List[str] = Field(...)

    createdBy: str = Field(...)
    createdAt: str = Field(...)
    dblpId: str = Field(...)

    class Config:
        """Configuration for the PaperModel."""

        use_enum_values = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "5136bc054aed4daf9e2a43203",
                "title": "Attention is all you need",
                "abstractText": (
                    "The dominant sequence transduction models are based on complex recurrent or"
                    " convolutional neural networks in an encoder-decoder configuration. The best"
                    " performing models also connect the encoder and decoder through an attention"
                    " mechanism. We propose a new simple network architecture, the Transformer,"
                    " based solely on attention mechanisms, dispensing with recurrence and"
                    " convolutions entirely. Experiments on two machine translation tasks show"
                    " these models to be superior in quality while being more parallelizable and"
                    " requiring significantly less time to train. Our model achieves 28.4 BLEU on"
                    " the WMT 2014 English-to-German translation task, improving over the existing"
                    " best results, including ensembles by over 2 BLEU. On the WMT 2014"
                    " English-to-French translation task, our model establishes a new single-model"
                    " state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight"
                    " GPUs, a small fraction of the training costs of the best models from the"
                    " literature. We show that the Transformer generalizes well to other tasks by"
                    " applying it successfully to English constituency parsing both with large and"
                    " limited training data."
                ),
                "abstractExtractor": "grobid",
                "typeOfPaper": "conference",
                "shortOrLong": "long",
                "atMainConference": True,
                "isSharedTask": False,
                "isStudentPaper": False,
                "doi": "10.5555/3295222.3295349",
                "preProcessingGitHash": "955ef880159216a23b7bfd13d3fb56eaa54b4113",
                "pdfUrl": "https://dl.acm.org/doi/pdf/10.5555/3295222.3295349",
                "absUrl": "https://dl.acm.org/doi/10.5555/3295222.3295349",
                "datePublished": datetime.today().isoformat(),
                "citationInfoTimestamp": datetime.today().isoformat(),
                "citedBy": [
                    "5136bc054aed4daf9e2a1231",
                    "5136bc054aed4daf9e2a1239",
                    "5136bc054aed4daf9e2a1237",
                    "5136bc054aed4daf9e2a1234",
                    "5136bc054aed4daf9e2a1232",
                    "5136bc054aed4daf9e2a1235",
                ],
                "authors": [
                    "5126bc054aed4daf9e2a1232",
                    "5126bc054aed4daf9e2a1233",
                    "5126bc054aed4daf9e2a1234",
                    "5126bc054aed4daf9e2a1235",
                    "5126bc054aed4daf9e2a1236",
                ],
                "firstAuthor": "5126bc054aed4daf9e2a1232",
                "venues": [
                    "5126bc054aed4daf9e2a1237",
                    "5126bc054aed4daf9e2a1238",
                    "5126bc054aed4daf9e2a1239",
                ],
                "createdBy": "507f1f77bcf86cd799439011",
                "createdAt": datetime.today().isoformat(),
                "dblpId": "whatever/id/it/is",
            }
        }
