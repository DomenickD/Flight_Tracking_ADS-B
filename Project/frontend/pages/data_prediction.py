"""This page will have a rudi prediction tool"""

import streamlit as st
import requests
import pandas as pd

# Static latitude and longitude
LATITUDE = 27.9506
LONGITUDE = -82.4572

st.subheader("ADS-B Category Prediction Tool")

# Input fields for relevant features in the ADS-B dataset

# Emergency status (binary encoding: 0 = none, 1 = emergency)
emergency_map = {"None": 0, "Emergency": 1}
emergency = st.selectbox("Emergency Status:", ["None", "Emergency"])

# Ground Speed (gs)
gs = st.slider("Ground Speed (knots):", 0.0, 1000.0, 350.0)

# Navigation Accuracy Category for Position (nac_p)
nac_p = st.slider("Navigation Accuracy Category (Position):", 0.0, 10.0, 5.0)

# Type of Aircraft (t)
aircraft_type = st.text_input("Aircraft Type (e.g., A320, B737, etc.):", value=90)

# Alert status (binary encoding: 0 = no alert, 1 = alert)
alert_map = {"No Alert": 0, "Alert": 1}
alert = st.selectbox("Alert Status:", ["No Alert", "Alert"])

# Barometric Rate (baro_rate)
baro_rate = st.slider("Barometric Rate (feet/min):", -6000.0, 6000.0, 0.0)

# Barometric Altitude (alt_baro)
alt_baro = st.slider("Barometric Altitude (feet):", 0.0, 45000.0, 10000.0)

# Track (degrees)
track = st.slider("Track (degrees):", 0.0, 360.0, 150.0)

# Geometric Altitude (alt_geom)
alt_geom = st.slider("Geometric Altitude (feet):", 0.0, 45000.0, 10000.0)

# Geometric Rate (geom_rate)
geom_rate = st.slider("Geometric Rate (feet/min):", -6000.0, 6000.0, 0.0)

# MCP/FCU Selected Altitude (nav_altitude_mcp)
nav_altitude_mcp = st.slider("MCP/FCU Selected Altitude (feet):", 0.0, 45000.0, 10000.0)

# Navigation Accuracy Category for Velocity (nac_v)
nac_v = st.slider("Navigation Accuracy Category (Velocity):", 0.0, 10.0, 5.0)

flight = st.text_input("Flight Number (Optional):", value="")
if flight == "":
    flight = 3032
hex_code = st.text_input("Hex Code (Optional):", value="")
if hex_code == "":
    hex_code = 2524

# User input dictionary to send to the API
user_input = {
    "lon": LONGITUDE,
    "emergency": emergency_map[emergency],
    "flight": flight,
    "nac_p": nac_p,
    "gs": gs,
    "t": aircraft_type,
    "alert": alert_map[alert],
    "baro_rate": baro_rate,
    "alt_baro": alt_baro,
    "track": track,
    "hex": hex_code,
    "alt_geom": alt_geom,
    "lat": LATITUDE,
    "geom_rate": geom_rate,
    "nav_altitude_mcp": nav_altitude_mcp,
    "nac_v": nac_v,
}

# Button to trigger the prediction
if st.button("Predict Category"):
    response = requests.post(
        "http://fastapi_route:8000/predict_adsb_category", json=user_input, timeout=15
    )

    if response.status_code == 200:
        result = response.json()
        predicted_category = result["category"]  # Now expecting a single label

        # Mapping the prediction to a readable category
        category_map = {
            "A0": "No ADS-B emitter category",
            "A1": "Light (< 15500 lbs)",
            "A2": "Small (15500 to 75000 lbs)",
            "A3": "Large (75000 to 300000 lbs)",
            "A4": "High vortex large (e.g., B-757)",
            "A5": "Heavy (> 300000 lbs)",
            "A6": "High performance (> 5g acceleration and 400 kts)",
            "A7": "Rotorcraft",
            "B0": "No ADS-B emitter category information",
            "B1": "Glider / sailplane",
            "B2": "Lighter-than-air",
            "B3": "Parachutist / skydiver",
            "B4": "Ultralight / hang-glider / paraglider",
            "B5": "Reserved",
            "B6": "Unmanned aerial vehicle",
        }

        # Display the predicted category
        st.write(
            f"Predicted Category: {category_map.get(predicted_category, 'Unknown')}"
        )
    else:
        st.error(f"Failed to get prediction: {response.status_code}")
        st.write(f"Error details: {response.text}")
