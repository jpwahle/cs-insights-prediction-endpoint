"""The production environment using uvicorn server."""
import argparse

import uvicorn  # type: ignore

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run the server in production mode.")

    parser.add_argument(
        "--workers", type=int, default=8, help="Number of workers to run the server with."
    )
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on.")

    args = parser.parse_args()

    uvicorn.run(
        "nlp_land_prediction_endpoint.app:app",
        host=args.host,
        port=args.port,
        workers=args.workers,
    )
