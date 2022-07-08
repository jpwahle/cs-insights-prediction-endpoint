"""This module implements the main app."""
from fastapi import FastAPI

import nlp_land_prediction_endpoint
from nlp_land_prediction_endpoint.middleware.forward_middleware import ForwardMiddleware
from nlp_land_prediction_endpoint.routes.route_auth import router as AuthRouter
from nlp_land_prediction_endpoint.routes.route_hosts import router as RemoteHostRouter
from nlp_land_prediction_endpoint.routes.route_model import router as ModelRouter
from nlp_land_prediction_endpoint.routes.route_status import router as StatusRouter
from nlp_land_prediction_endpoint.routes.route_topic import router as TopicRouter
from nlp_land_prediction_endpoint.utils import settings as Settings
from nlp_land_prediction_endpoint.utils.version_getter import get_backend_version

# if not os.path.exists("./.env"):
#     print("======== No .env file found ========")
#     print("= Copy the contents of sample.env  =")
#     print("= to .env in the root directory    =")
#     print("= and change the contents!         =")
#     print("====================================")
#     os.environ["AUTH_BACKEND_VERSION"] = "v0"
#     os.environ["AUTH_BACKEND_URL"] = "http://127.0.0.1/api/{version}"
#     os.environ["AUTH_BACKEND_LOGIN_ROUTE"] = "/auth/login/service"
#     os.environ["AUTH_TOKEN_ROUTE"] = "/auth/service"
#     os.environ["JWT_SECRET"] = "super_secret_secret"
#     os.environ["JWT_TOKEN_EXPIRATION_MINUTES"] = "30"
#     os.environ["JWT_SIGN_ALG"] = "HS256"
#     os.environ["NODE_TYPE"] = "SECONDARY"
#
# print(os.environ)


app = FastAPI(title="NLP-Land-prediction-endpoint", docs_url="/api/docs", redoc_url="/api/redoc")


settings = Settings.get_settings()

if "{version}" in settings.AUTH_BACKEND_URL:
    get_backend_version()

app.add_middleware(ForwardMiddleware)

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
