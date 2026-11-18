"""Streamlit interface for the existing house price prediction model."""

from pathlib import Path

import joblib
import numpy as np
import streamlit as st


MODEL_PATH = Path(__file__).resolve().parent / "house_price_model.pkl"


@st.cache_resource
def load_model():
    """Load and cache the trained model so it is reused across UI reruns."""
    return joblib.load(MODEL_PATH)


st.set_page_config(
    page_title="House Price Prediction System",
    page_icon="🏠",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f7f9fc 0%, #edf4ff 100%);
    }
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 3rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("House Price Prediction System")
st.subheader("Machine Learning Powered House Price Estimation")
st.write(
    "Enter the property details below to estimate its price in Indian lakhs."
)

try:
    model = load_model()
except FileNotFoundError:
    st.error(
        "The trained model file was not found. Make sure "
        "`house_price_model.pkl` is in the project folder."
    )
    st.stop()
except Exception as exc:
    st.error("The trained model could not be loaded: {}".format(exc))
    st.stop()

st.header("House details")
area_column, bedroom_column, age_column = st.columns(3)

with area_column:
    area = st.number_input(
        "Area of House (square feet)",
        min_value=0.0,
        value=2000.0,
        step=100.0,
    )

with bedroom_column:
    bedrooms = st.number_input(
        "Number of Bedrooms",
        min_value=1,
        value=3,
        step=1,
    )

with age_column:
    age = st.number_input(
        "Age of House (years)",
        min_value=0.0,
        value=5.0,
        step=1.0,
    )

if st.button("Predict House Price", type="primary"):
    if area <= 0:
        st.error("Area must be greater than zero.")
    elif bedrooms < 1:
        st.error("Number of bedrooms must be at least one.")
    elif age < 0:
        st.error("Age of the house cannot be negative.")
    else:
        try:
            # Keep the feature order used when the existing model was trained.
            features = np.array([[area, bedrooms, age]], dtype=float)
            predicted_price = float(model.predict(features)[0])
            if not np.isfinite(predicted_price):
                raise ValueError("The model returned a non-finite prediction.")
            st.success(
                "Predicted House Price: ₹ {:.2f} Lakhs".format(predicted_price)
            )
        except Exception as exc:
            st.error("Unable to generate a prediction: {}".format(exc))
