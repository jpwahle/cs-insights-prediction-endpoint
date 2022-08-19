"""This module implements the main app."""
from fastapi import FastAPI

import cs_insights_prediction_endpoint

# from cs_insights_prediction_endpoint.middleware.forward_middleware import ForwardMiddleware
from cs_insights_prediction_endpoint.routes.route_auth import router as auth_router
from cs_insights_prediction_endpoint.routes.route_hosts import (
    router as remote_host_router,
)
from cs_insights_prediction_endpoint.routes.route_model import router as model_router
from cs_insights_prediction_endpoint.routes.route_model_forward import (
    router as model_forward_router,
)
from cs_insights_prediction_endpoint.routes.route_status import router as status_router
from cs_insights_prediction_endpoint.routes.route_topic import router as topic_router
from cs_insights_prediction_endpoint.utils.settings import get_settings
from cs_insights_prediction_endpoint.utils.version_getter import get_backend_version

app = FastAPI(
    title="cs-insights-prediction-endpoint",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

settings = get_settings()

if "{version}" in settings.auth_backend_url:
    get_backend_version()

app.include_router(
    status_router,
    tags=["Status"],
    prefix=f"/api/v{cs_insights_prediction_endpoint.__version__.split('.')[0]}/status",
)

app.include_router(
    topic_router,
    tags=["Topics"],
    prefix=f"/api/v{cs_insights_prediction_endpoint.__version__.split('.')[0]}/topics",
)

if settings.node_type == "MAIN":
    app.include_router(
        model_forward_router,
        tags=["ModelForward"],
        prefix=f"/api/v{cs_insights_prediction_endpoint.__version__.split('.')[0]}/models",
    )

    app.include_router(
        remote_host_router,
        tags=["Hosts"],
        prefix=f"/api/v{cs_insights_prediction_endpoint.__version__.split('.')[0]}/hosts",
    )

else:
    app.include_router(
        model_router,
        tags=["Model"],
        prefix=f"/api/v{cs_insights_prediction_endpoint.__version__.split('.')[0]}/models",
    )

app.include_router(
    auth_router,
    tags=["Auth"],
    prefix=f"/api/v{cs_insights_prediction_endpoint.__version__.split('.')[0]}/auth",
)
