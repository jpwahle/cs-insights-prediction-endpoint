"""The development environment using uvicorn server."""
import uvicorn  # type: ignore

if __name__ == "__main__":
    uvicorn.run("cs_insights_prediction_endpoint.app:app", host="0.0.0.0", port=8000, reload=True)
