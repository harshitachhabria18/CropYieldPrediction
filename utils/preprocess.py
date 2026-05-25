# ============================================
# utils/preprocess.py — Input cleaning & rainfall fetching
# ============================================

import requests
from config import STATE_COORDINATES, OPEN_METEO_URL


def fetch_annual_rainfall(state, crop_year):
    """
    Fetches the total annual rainfall (mm) for a given state and crop year
    using the Open-Meteo historical weather API.
    """

    # Step 1 — Get coordinates for the state
    if state not in STATE_COORDINATES:
        raise ValueError(f"State '{state}' not found in STATE_COORDINATES.")

    lat, lon = STATE_COORDINATES[state]

    # Step 2 — Build date range for the full crop year
    start_date = f"{crop_year}-01-01"
    end_date   = f"{crop_year}-12-31"

    # Step 3 — Build request parameters
    params = {
        "latitude":   lat,
        "longitude":  lon,
        "start_date": start_date,
        "end_date":   end_date,
        "daily":      "precipitation_sum",
        "timezone":   "Asia/Kolkata"
    }

    # Step 4 — Call Open-Meteo API
    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Weather API request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Weather API request failed: {e}")

    # Step 5 — Parse and sum daily precipitation
    data = response.json()

    daily_rainfall = data.get("daily", {}).get("precipitation_sum", [])

    if not daily_rainfall:
        raise RuntimeError("No rainfall data returned from the API.")

    # Sum all daily values, skip None entries
    annual_rainfall = sum(v for v in daily_rainfall if v is not None)

    return round(annual_rainfall, 2)


def clean_inputs(crop, season, state):
    """
    Cleans categorical inputs to match training data format.
    Applies strip + title case — same as preprocessing done during training.
    """
    crop   = crop.strip().title()
    season = season.strip().title()
    state  = state.strip().title()

    return crop, season, state


def validate_numerical_inputs(area, fertilizer, pesticide):
    """
    Validates that numerical inputs are positive.
    """
    if area <= 0:
        raise ValueError("Area must be greater than 0.")
    if fertilizer < 0:
        raise ValueError("Fertilizer value cannot be negative.")
    if pesticide < 0:
        raise ValueError("Pesticide value cannot be negative.")