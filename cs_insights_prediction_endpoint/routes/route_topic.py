"""This module implements the endpoint logic for topics."""
from fastapi import APIRouter, status

from cs_insights_prediction_endpoint.models.model_paper import PaperModel
from cs_insights_prediction_endpoint.models.model_topic import TopicResponseModel

router = APIRouter()


@router.post(
    "/",
    response_description="Topics for a single paper.",
    response_model=TopicResponseModel,
    status_code=status.HTTP_200_OK,
)
async def topic_for_papers(
    paper: PaperModel,
) -> TopicResponseModel:
    """Generate topics for a set of papers.

    Args:
        paper (PaperModel): The paper objects to analyse.

    Returns:
        TopicResponseModel: The response object for the computed topics.
    """
    # Do some stuff with the data
    # paper_ids = [paper["id"] for paper in papers]

    # Craft the response
    return TopicResponseModel(
        topics=[
            {
                "id": "5136bc054aed4daf9e2a1237",
                "name": "Topic 1",
                "score": 0.5,
                "keywords": ["keyword 1", "keyword 2"],
                "paper_ids": ["5136bc054aed4daf9e2a1239", "5136bc054aed4daf9e2a1238"],
            },
        ],
    )
