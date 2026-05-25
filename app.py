# ============================================
# app.py — Streamlit Frontend for Crop Yield Prediction
# ============================================

import streamlit as st
import sys
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import (
    CROPS, SEASONS, STATES,
    CROP_YEAR_MIN, CROP_YEAR_MAX,
    AREA_MIN, AREA_MAX,
    FERTILIZER_MIN, FERTILIZER_MAX,
    PESTICIDE_MIN, PESTICIDE_MAX,
    GROQ_MODEL, GROQ_MAX_TOKENS
)
from utils.predict import predict_crop_yield

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="Crop Yield Predictor",
    page_icon="🌾",
    layout="centered"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Source Sans 3', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Merriweather', serif;
        }

        .main {
            background-color: #f5f0e8;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        .stButton > button {
            background-color: #4a7c59;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            width: 100%;
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #355c42;
            color: white;
        }

        .result-box {
            background-color: #e8f5e9;
            border-left: 5px solid #4a7c59;
            border-radius: 8px;
            padding: 1.2rem 1.5rem;
            margin-top: 1.5rem;
        }

        .rainfall-box {
            background-color: #e3f2fd;
            border-left: 5px solid #1976d2;
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin-top: 1rem;
        }

        .summary-box {
            background-color: #F8FAFC;
            border-left: 5px solid #94A3B8;
            border-radius: 8px;
            padding: 1.2rem 1.5rem;
            margin-top: 1rem;
        }

        .error-box {
            background-color: #ffebee;
            border-left: 5px solid #c62828;
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin-top: 1rem;
        }

        .section-header {
            color: #355c42;
            font-size: 1rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem;
            margin-top: 1.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================
# GROQ SUMMARY FUNCTION
# ============================================

def generate_summary(crop, crop_year, season, state, area, fertilizer, pesticide, annual_rainfall, prediction):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are an expert agricultural analyst. Based on the following crop details and predicted yield, provide a concise analysis in 4-5 sentences.

Crop Details:
- Crop: {crop}
- Season: {season}
- State: {state}
- Crop Year: {crop_year}
- Area: {area} hectares
- Annual Rainfall: {annual_rainfall} mm
- Fertilizer Used: {fertilizer} kg
- Pesticide Used: {pesticide} kg
- Predicted Yield: {prediction} kg/hectare

Your analysis should cover:
1. Whether the predicted yield is high, moderate, or low for this crop in India
2. How the rainfall level may have impacted the yield
3. Whether the fertilizer and pesticide usage seems appropriate
4. One or two practical recommendations to improve yield

Keep the tone helpful, simple, and farmer-friendly.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=GROQ_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ============================================
# HEADER
# ============================================

st.markdown("## 🌾 Crop Yield Predictor")
st.markdown("Enter the crop details below. Annual rainfall will be **automatically fetched** based on the state and year selected.")
st.divider()

# ============================================
# INPUT FORM
# ============================================

st.markdown('<p class="section-header">📋 Crop Details</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    crop = st.selectbox("Crop", options=CROPS)

with col2:
    season = st.selectbox("Season", options=SEASONS)

col3, col4 = st.columns(2)

with col3:
    state = st.selectbox("State", options=STATES)

with col4:
    crop_year = st.slider(
        "Crop Year",
        min_value=CROP_YEAR_MIN,
        max_value=CROP_YEAR_MAX,
        value=2015,
        step=1
    )

st.markdown('<p class="section-header">📐 Field & Input Quantities</p>', unsafe_allow_html=True)

col5, col6, col7 = st.columns(3)

with col5:
    area = st.number_input(
        "Area (hectares)",
        min_value=float(AREA_MIN),
        max_value=float(AREA_MAX),
        value=1000.0,
        step=100.0,
        help="Total area under cultivation in hectares"
    )

with col6:
    fertilizer = st.number_input(
        "Fertilizer (kg)",
        min_value=float(FERTILIZER_MIN),
        max_value=float(FERTILIZER_MAX),
        value=10000.0,
        step=500.0,
        help="Total fertilizer used in kg"
    )

with col7:
    pesticide = st.number_input(
        "Pesticide (kg)",
        min_value=float(PESTICIDE_MIN),
        max_value=float(PESTICIDE_MAX),
        value=100.0,
        step=10.0,
        help="Total pesticide used in kg"
    )

st.markdown("")

# ============================================
# PREDICT BUTTON
# ============================================

if st.button("🌱 Predict Yield"):

    with st.spinner(f"Fetching rainfall data for {state} ({crop_year})..."):

        try:
            prediction, annual_rainfall = predict_crop_yield(
                crop=crop,
                crop_year=crop_year,
                season=season,
                state=state,
                area=area,
                fertilizer=fertilizer,
                pesticide=pesticide
            )

            # Rainfall result
            st.markdown(f"""
                <div class="rainfall-box">
                    🌧️ <strong>Annual Rainfall Fetched:</strong> {annual_rainfall} mm
                    &nbsp;&nbsp;|&nbsp;&nbsp; 📍 {state} &nbsp;&nbsp;|&nbsp;&nbsp; 📅 {crop_year}
                </div>
            """, unsafe_allow_html=True)

            # Prediction result
            st.markdown(f"""
                <div class="result-box">
                    ✅ <strong>Predicted Crop Yield</strong><br>
                    <span style="font-size: 2rem; font-weight: 700; color: #2e7d32;">{prediction} kg/hectare</span><br>
                    <span style="color: #555; font-size: 0.9rem;">Crop: {crop} &nbsp;|&nbsp; Season: {season} &nbsp;|&nbsp; State: {state} &nbsp;|&nbsp; Year: {crop_year}</span>
                </div>
            """, unsafe_allow_html=True)

            # Groq AI Summary
            with st.spinner("Generating AI analysis..."):
                try:
                    summary = generate_summary(
                        crop=crop,
                        crop_year=crop_year,
                        season=season,
                        state=state,
                        area=area,
                        fertilizer=fertilizer,
                        pesticide=pesticide,
                        annual_rainfall=annual_rainfall,
                        prediction=prediction
                    )

                    st.markdown(f"""
                        <div class="summary-box">
                            <strong>💡 AI Analysis</strong><br><br>
                            <span style="color: #444; font-size: 0.95rem; line-height: 1.7;">{summary}</span>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.markdown(f"""
                        <div class="error-box">
                            ⚠️ <strong>AI Summary Error:</strong> {e}
                        </div>
                    """, unsafe_allow_html=True)

        except RuntimeError as e:
            st.markdown(f"""
                <div class="error-box">
                    ⚠️ <strong>Weather API Error:</strong> {e}
                </div>
            """, unsafe_allow_html=True)

        except ValueError as e:
            st.markdown(f"""
                <div class="error-box">
                    ⚠️ <strong>Input Error:</strong> {e}
                </div>
            """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.divider()
st.markdown(
    "<p style='text-align:center; color:#999; font-size:0.85rem;'>Rainfall data sourced from Open-Meteo Historical API &nbsp;|&nbsp; AI Analysis powered by Groq &nbsp;|&nbsp; Model trained on Indian crop yield dataset (1997–2020)</p>",
    unsafe_allow_html=True
)