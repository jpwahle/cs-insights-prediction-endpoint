"""This module implements the main app."""
from fastapi import FastAPI

import nlp_land_prediction_endpoint
from nlp_land_prediction_endpoint.routes.route_auth import router as AuthRouter

# from nlp_land_prediction_endpoint.middleware.auth import check_auth
from nlp_land_prediction_endpoint.routes.route_status import router as StatusRouter
from nlp_land_prediction_endpoint.routes.route_topic import router as TopicRouter

app = FastAPI(title="NLP-Land-prediction-endpoint", docs_url="/api/docs", redoc_url="/api/redoc")

# app.add_event_handler("startup", connect_to_third_party_services)
# app.add_event_handler("shutdown", close_third_party_services)

app.include_router(
    StatusRouter,
    tags=["Status"],
    prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/status",
)

app.include_router(
    TopicRouter,
    tags=["Topics"],
    prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/topics",
)

app.include_router(
    AuthRouter,
    tags=["Auth"],
    prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/auth",
)
