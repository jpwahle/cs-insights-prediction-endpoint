"""This module implements the main app."""
from fastapi import FastAPI

import nlp_land_prediction_endpoint

# from nlp_land_prediction_endpoint.middleware.forward_middleware import ForwardMiddleware
from nlp_land_prediction_endpoint.routes.route_auth import router as AuthRouter
from nlp_land_prediction_endpoint.routes.route_hosts import router as RemoteHostRouter
from nlp_land_prediction_endpoint.routes.route_model import router as ModelRouter
from nlp_land_prediction_endpoint.routes.route_model_forward import (
    router as ModelForwardRouter,
)
from nlp_land_prediction_endpoint.routes.route_status import router as StatusRouter
from nlp_land_prediction_endpoint.routes.route_topic import router as TopicRouter
from nlp_land_prediction_endpoint.utils.settings import get_settings
from nlp_land_prediction_endpoint.utils.version_getter import get_backend_version

app = FastAPI(
    title="NLP-Land-prediction-endpoint",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)


settings = get_settings()
print(get_settings().NODE_TYPE)

if "{version}" in settings.AUTH_BACKEND_URL:
    get_backend_version()

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

if settings.NODE_TYPE == "MAIN":
    app.include_router(
        ModelForwardRouter,
        tags=["ModelForward"],
        prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/models",
    )
else:
    app.include_router(
        ModelRouter,
        tags=["Model"],
        prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/models",
    )

    app.include_router(
        RemoteHostRouter,
        tags=["Hosts"],
        prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/hosts",
    )


app.include_router(
    AuthRouter,
    tags=["Auth"],
    prefix=f"/api/v{nlp_land_prediction_endpoint.__version__.split('.')[0]}/auth",
)
