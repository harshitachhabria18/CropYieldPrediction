# ============================================
# utils/predict.py — Model loading & prediction
# ============================================

import joblib
import pandas as pd
from config import MODEL_PATH, FEATURES
from utils.preprocess import fetch_annual_rainfall, clean_inputs, validate_numerical_inputs


# Load model once when the module is imported
model = joblib.load(MODEL_PATH)


def predict_crop_yield(crop, crop_year, season, state, area, fertilizer, pesticide):
    """
    Predicts crop yield (kg/hectare) for the given inputs.

    Steps:
        1. Clean categorical inputs
        2. Validate numerical inputs
        3. Fetch annual rainfall from Open-Meteo API
        4. Build input dataframe
        5. Run model prediction and return result
    """

    # Step 1 — Clean categorical inputs
    crop, season, state = clean_inputs(crop, season, state)

    # Step 2 — Validate numerical inputs
    validate_numerical_inputs(area, fertilizer, pesticide)

    # Step 3 — Fetch annual rainfall automatically
    annual_rainfall = fetch_annual_rainfall(state, crop_year)

    # Step 4 — Build input dataframe in the same column order as training
    input_data = pd.DataFrame([{
        "Crop":             crop,
        "Crop_Year":        crop_year,
        "Season":           season,
        "State":            state,
        "Area":             area,
        "Annual_Rainfall":  annual_rainfall,
        "Fertilizer":       fertilizer,
        "Pesticide":        pesticide
    }])[FEATURES]

    # Step 5 — Predict and return
    prediction = model.predict(input_data)[0]

    return round(prediction, 2), annual_rainfall