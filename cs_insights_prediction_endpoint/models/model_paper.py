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


class paper_model(BaseModel):
    """The model for a paper. Should be identical to the NLP-Land-backend.

    Args:
        BaseModel (Any): Base class of FastAPI models.
    """

    id: str = Field(...)
    title: str = Field(...)
    abstract_text: str = Field(...)
    abstract_extractor: ExtractionMethod = Field(...)
    type_of_paper: TypeOfPaper = Field(...)
    short_long: ShortLong = Field(...)

    at_main_conference: bool = Field(...)
    is_shared_task: bool = Field(...)
    is_student_paper: bool = Field(...)

    doi: str = Field(...)
    pre_processing_git_hash: str = Field(...)
    pdf_url: AnyUrl = Field(...)
    abs_url: AnyUrl = Field(...)

    date_published: str = Field(...)
    citation_info_timestamp: str = Field(...)
    cited_by: List[str] = Field(...)

    authors: List[str] = Field(...)
    first_author: str = Field(...)
    venues: List[str] = Field(...)

    created_by: str = Field(...)
    created_at: str = Field(...)
    dblp_id: str = Field(...)

    class Config:
        """Configuration for the paper_model."""

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
                "type_of_paper": "conference",
                "short_or_long": "long",
                "at_main_conference": True,
                "is_shared_task": False,
                "is_student_paper": False,
                "doi": "10.5555/3295222.3295349",
                "pre_processing_git_hash": "955ef880159216a23b7bfd13d3fb56eaa54b4113",
                "pdf_url": "https://dl.acm.org/doi/pdf/10.5555/3295222.3295349",
                "abs_url": "https://dl.acm.org/doi/10.5555/3295222.3295349",
                "date_published": datetime.today().isoformat(),
                "citation_info_timestamp": datetime.today().isoformat(),
                "cited_by": [
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
                "first_author": "5126bc054aed4daf9e2a1232",
                "venues": [
                    "5126bc054aed4daf9e2a1237",
                    "5126bc054aed4daf9e2a1238",
                    "5126bc054aed4daf9e2a1239",
                ],
                "created_by": "507f1f77bcf86cd799439011",
                "created_at": datetime.today().isoformat(),
                "dblp_id": "whatever/id/it/is",
            }
        }
