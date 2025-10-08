"""
app.py
------
Flask web application for serving hotel reservation predictions.

This module:
1) Instantiates a Flask app and loads the trained model artifact.
2) Exposes a single route ('/') which renders a simple form and, on POST,
   parses user inputs, performs prediction, and returns the result to the template.

Usage
-----
Run locally (development):
    python app.py

Then open the app in your browser:
    http://127.0.0.1:8080

Notes
-----
- The model artefact path is configured via `config.paths_config.MODEL_OUTPUT_PATH`.
- Errors are logged using the project-wide logger and surfaced cleanly.
- Input parsing is intentionally explicit to mirror the expected form fields
  and preserve the model's feature ordering.
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
from typing import Callable, Optional, Any

# -------------------------------------------------------------------
# Third-Party Imports
# -------------------------------------------------------------------
import joblib
import numpy as np
from flask import Flask, render_template, request

# -------------------------------------------------------------------
# Internal Imports
# -------------------------------------------------------------------
from config.paths_config import MODEL_OUTPUT_PATH
from src.logger import get_logger
from src.custom_exception import CustomException

# -------------------------------------------------------------------
# App & Logger Setup
# -------------------------------------------------------------------
app: Flask = Flask(__name__)
logger = get_logger(__name__)

# -------------------------------------------------------------------
# Model Loading
# -------------------------------------------------------------------
def _load_model(model_path: str) -> Any:
    """
    Load a serialised model artefact using joblib.

    Parameters
    ----------
    model_path : str
        Filesystem path to the trained model artefact.

    Returns
    -------
    Any
        The loaded model object.

    Raises
    ------
    CustomException
        If the model cannot be loaded for any reason.
    """
    try:
        logger.info(f"Loading model artefact from: {model_path}")
        model = joblib.load(model_path)
        logger.info("Model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Failed to load model from '{model_path}': {e}")
        import sys
        raise CustomException("Unable to load the trained model artefact.", sys) from e


# Load once at import time for performance
loaded_model = _load_model(MODEL_OUTPUT_PATH)


# -------------------------------------------------------------------
# Helpers: Input Parsing
# -------------------------------------------------------------------
def _parse_field(
    form_key: str,
    caster: Callable[[str], Any],
    *,
    default: Optional[Any] = None
) -> Any:
    """
    Safely parse and cast a field from Flask's request.form.

    Parameters
    ----------
    form_key : str
        Key expected in `request.form`.
    caster : Callable[[str], Any]
        Function to cast the string value (e.g., int, float).
    default : Optional[Any], optional
        Fallback value when the key is missing or blank. Defaults to None.

    Returns
    -------
    Any
        The cast value or the provided default.

    Raises
    ------
    ValueError
        If the value is present but cannot be cast using the provided caster.
    """
    raw = request.form.get(form_key, "")
    if raw == "":
        # Mirror original behaviour (which expects presence of form fields)
        # but allow a default to avoid hard crashes if template evolves.
        if default is not None:
            return default
        raise ValueError(f"Missing required form field: '{form_key}'")
    try:
        return caster(raw)
    except Exception as e:
        raise ValueError(f"Invalid value for '{form_key}': {raw} ({e})") from e


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the input form (GET) or make a prediction from form inputs (POST).

    Form fields expected (names must match the HTML template):
    - lead_time : int
    - no_of_special_request : int
    - avg_price_per_room : float
    - arrival_month : int
    - arrival_date : int
    - market_segment_type : int
    - no_of_week_nights : int
    - no_of_weekend_nights : int
    - type_of_meal_plan : int
    - room_type_reserved : int

    Returns
    -------
    flask.Response
        Rendered HTML template ('index.html') with an optional prediction.
    """
    if request.method == "POST":
        try:
            # -----------------------------------------------------------
            # 1) Extract and cast inputs from the form
            #    Keep the order aligned with the model's expected features.
            # -----------------------------------------------------------
            lead_time: int = _parse_field("lead_time", int)
            no_of_special_request: int = _parse_field("no_of_special_request", int)
            avg_price_per_room: float = _parse_field("avg_price_per_room", float)
            arrival_month: int = _parse_field("arrival_month", int)
            arrival_date: int = _parse_field("arrival_date", int)

            market_segment_type: int = _parse_field("market_segment_type", int)
            no_of_week_nights: int = _parse_field("no_of_week_nights", int)
            no_of_weekend_nights: int = _parse_field("no_of_weekend_nights", int)

            type_of_meal_plan: int = _parse_field("type_of_meal_plan", int)
            room_type_reserved: int = _parse_field("room_type_reserved", int)

            # -----------------------------------------------------------
            # 2) Construct the feature array with the exact shape (1, 10)
            # -----------------------------------------------------------
            features: np.ndarray = np.array(
                [
                    [
                        lead_time,
                        no_of_special_request,
                        avg_price_per_room,
                        arrival_month,
                        arrival_date,
                        market_segment_type,
                        no_of_week_nights,
                        no_of_weekend_nights,
                        type_of_meal_plan,
                        room_type_reserved,
                    ]
                ],
                dtype=float,  # cast to float to be universally acceptable for most models
            )

            logger.info(f"Received features for prediction: {features.tolist()}")

            # -----------------------------------------------------------
            # 3) Predict
            # -----------------------------------------------------------
            prediction = loaded_model.predict(features)
            logger.info(f"Model prediction: {prediction}")

            # -----------------------------------------------------------
            # 4) Render result
            # -----------------------------------------------------------
            return render_template("index.html", prediction=prediction[0])

        except Exception as e:
            # Log the error and surface a clean message to the user via the template
            logger.error(f"Prediction request failed: {e}")
            # You may choose to pass an error message to the template if it supports it
            # e.g., return render_template("index.html", prediction=None, error=str(e))
            return render_template("index.html", prediction=None)

    # GET: initial page load (no prediction)
    return render_template("index.html", prediction=None)


# -------------------------------------------------------------------
# Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Bind to all interfaces for containerised / remote access; keep port 8080 as specified.
    app.run(host="0.0.0.0", port=8080)