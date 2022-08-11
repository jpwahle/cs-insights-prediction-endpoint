"""This helper will generate the documentation opeanapi json file."""
import json

from cs_insights_prediction_endpoint.app import app

oas_dict = app.openapi()

with open("docs/oas.json", "w") as fp:
    json.dump(oas_dict, fp)
