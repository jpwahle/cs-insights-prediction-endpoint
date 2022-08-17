"""This module implements the endpoint logic for topics."""
from fastapi import APIRouter, status

from cs_insights_prediction_endpoint.models.model_paper import paper_model
from cs_insights_prediction_endpoint.models.model_topic import topic_response_model

router = APIRouter()


@router.post(
    "/",
    response_description="Topics for a single paper.",
    response_model=topic_response_model,
    status_code=status.HTTP_200_OK,
)
async def topic_for_papers(
    paper: paper_model,
) -> topic_response_model:
    """Generate topics for a set of papers.

    Args:
        paper (paper_model): The paper objects to analyse.

    Returns:
        topic_response_model: The response object for the computed topics.
    """
    # Do some stuff with the data
    # paper_ids = [paper["id"] for paper in papers]

    # Craft the response
    return topic_response_model(
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
