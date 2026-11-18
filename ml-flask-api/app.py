"""Flask REST API for the sample house price prediction model."""

from pathlib import Path
from numbers import Real

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

print("Starting Flask API for house price prediction model...")

app = Flask(__name__)
MODEL_PATH = Path(__file__).resolve().parent / "house_price_model.pkl"
FEATURE_NAMES = ("area", "bedrooms", "age")
_model = None


def get_model():
    """Load the model on the first prediction request."""
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


@app.get("/")
def home():
    return jsonify({"message": "Welcome to House Price Prediction API"})


@app.post("/predict")
def predict():
    try:
        data = request.get_json()
    except UnsupportedMediaType:
        return jsonify({"error": "Content-Type must be application/json."}), 415
    except BadRequest:
        return jsonify({"error": "Request body must contain valid JSON."}), 400

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body must be an object."}), 400

    missing_features = [name for name in FEATURE_NAMES if name not in data]
    if missing_features:
        return jsonify(
            {
                "error": "Missing required input feature(s).",
                "missing_features": missing_features,
            }
        ), 400

    values = {}
    for name in FEATURE_NAMES:
        value = data[name]
        if isinstance(value, bool) or not isinstance(value, Real):
            return jsonify(
                {"error": "Input feature '{}' must be numeric.".format(name)}
            ), 400
        if not np.isfinite(value):
            return jsonify(
                {"error": "Input feature '{}' must be a finite number.".format(name)}
            ), 400
        values[name] = value

    if values["area"] <= 0:
        return jsonify({"error": "Input feature 'area' must be greater than zero."}), 400
    if values["bedrooms"] < 1 or not float(values["bedrooms"]).is_integer():
        return jsonify(
            {"error": "Input feature 'bedrooms' must be a positive whole number."}
        ), 400
    if values["age"] < 0:
        return jsonify({"error": "Input feature 'age' cannot be negative."}), 400

    try:
        model = get_model()
    except FileNotFoundError:
        return jsonify(
            {
                "error": "Trained model file is missing. Run 'python train_model.py' first."
            }
        ), 503

    features = pd.DataFrame(
        [[values[name] for name in FEATURE_NAMES]], columns=FEATURE_NAMES
    )
    prediction = float(model.predict(features)[0])
    return jsonify({"prediction": round(prediction, 2)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
