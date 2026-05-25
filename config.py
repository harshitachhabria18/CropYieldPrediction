# ============================================
# CONFIG.PY — Central configuration file
# ============================================

# Model path
MODEL_PATH = "model/crop_yield_pipeline.pkl"

# Feature columns (must match training order)
FEATURES = [
    "Crop",
    "Crop_Year",
    "Season",
    "State",
    "Area",
    "Annual_Rainfall",
    "Fertilizer",
    "Pesticide"
]

TARGET = "Yield"

# ============================================
# DROPDOWN VALUES (extracted from dataset)
# ============================================

CROPS = [
    'Arecanut', 'Arhar/Tur', 'Bajra', 'Banana', 'Barley',
    'Black Pepper', 'Cardamom', 'Cashewnut', 'Castor Seed', 'Coconut',
    'Coriander', 'Cotton(Lint)', 'Cowpea(Lobia)', 'Dry Chillies', 'Garlic',
    'Ginger', 'Gram', 'Groundnut', 'Guar Seed', 'Horse-Gram',
    'Jowar', 'Jute', 'Khesari', 'Linseed', 'Maize',
    'Masoor', 'Mesta', 'Moong(Green Gram)', 'Moth', 'Niger Seed',
    'Oilseeds Total', 'Onion', 'Other  Rabi Pulses', 'Other Cereals', 'Other Kharif Pulses',
    'Other Oilseeds', 'Other Summer Pulses', 'Peas & Beans (Pulses)', 'Potato', 'Ragi',
    'Rapeseed &Mustard', 'Rice', 'Safflower', 'Sannhamp', 'Sesamum',
    'Small Millets', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet Potato',
    'Tapioca', 'Tobacco', 'Turmeric', 'Urad', 'Wheat'
]

SEASONS = [
    'Autumn', 'Kharif', 'Rabi', 'Summer', 'Whole Year', 'Winter'
]

STATES = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
    'Jammu And Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
    'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
    'Odisha', 'Puducherry', 'Punjab', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]

# ============================================
# STATE COORDINATES (for Open-Meteo API)
# ============================================

STATE_COORDINATES = {
    'Andhra Pradesh':       (15.9129,  79.7400),
    'Arunachal Pradesh':    (28.2180,  94.7278),
    'Assam':                (26.2006,  92.9376),
    'Bihar':                (25.0961,  85.3131),
    'Chhattisgarh':         (21.2787,  81.8661),
    'Delhi':                (28.7041,  77.1025),
    'Goa':                  (15.2993,  74.1240),
    'Gujarat':              (22.2587,  71.1924),
    'Haryana':              (29.0588,  76.0856),
    'Himachal Pradesh':     (31.1048,  77.1734),
    'Jammu And Kashmir':    (33.7782,  76.5762),
    'Jharkhand':            (23.6102,  85.2799),
    'Karnataka':            (15.3173,  75.7139),
    'Kerala':               (10.8505,  76.2711),
    'Madhya Pradesh':       (22.9734,  78.6569),
    'Maharashtra':          (19.7515,  75.7139),
    'Manipur':              (24.6637,  93.9063),
    'Meghalaya':            (25.4670,  91.3662),
    'Mizoram':              (23.1645,  92.9376),
    'Nagaland':             (26.1584,  94.5624),
    'Odisha':               (20.9517,  85.0985),
    'Puducherry':           (11.9416,  79.8083),
    'Punjab':               (31.1471,  75.3412),
    'Sikkim':               (27.5330,  88.5122),
    'Tamil Nadu':           (11.1271,  78.6569),
    'Telangana':            (18.1124,  79.0193),
    'Tripura':              (23.9408,  91.9882),
    'Uttar Pradesh':        (26.8467,  80.9462),
    'Uttarakhand':          (30.0668,  79.0193),
    'West Bengal':          (22.9868,  87.8550),
}

# ============================================
# OPEN-METEO API CONFIG
# ============================================

OPEN_METEO_URL = "https://archive-api.open-meteo.com/v1/archive"

# ============================================
# GROQ LLM CONFIG
# ============================================

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MAX_TOKENS = 512

# ============================================
# NUMERICAL RANGES (for input validation)
# ============================================

CROP_YEAR_MIN = 1997
CROP_YEAR_MAX = 2020

AREA_MIN = 0.5
AREA_MAX = 50808100.0

FERTILIZER_MIN = 54.17
FERTILIZER_MAX = 4835406877.0

PESTICIDE_MIN = 0.09
PESTICIDE_MAX = 15750511.0