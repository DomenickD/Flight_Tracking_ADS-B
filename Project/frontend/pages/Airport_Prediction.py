"""Predict Airport Locations based on flight adsb data"""

import requests
import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
from streamlit_folium import folium_static


X_test = pd.read_csv("airport_pred_X_test.csv")
X_test = X_test.drop(["airport_name", "Unnamed: 0"], axis=1)

# X_test = pd.DataFrame(data)
st.dataframe(X_test)

st.subheader("ADS-B Category Prediction Tool")

# Display the X_test DataFrame and allow users to select a row
selected_row = st.selectbox(
    "Select a row from X_test to autofill the form:", X_test.index
)

# Auto-fill sliders with the selected row's values
alt_baro = st.slider(
    "Barometric Altitude (feet):", 0.0, 45000.0, X_test.loc[selected_row, "alt_baro"]
)
nav_altitude_mcp = st.slider(
    "MCP/FCU Selected Altitude (feet):",
    0.0,
    45000.0,
    X_test.loc[selected_row, "nav_altitude_mcp"],
)
gs = st.slider("Ground Speed (knots):", 0.0, 1000.0, X_test.loc[selected_row, "gs"])
geom_rate = st.slider(
    "Geometric Rate (feet/min):", -6000.0, 6000.0, X_test.loc[selected_row, "geom_rate"]
)
lat = st.slider("Latitude:", -90.0, 90.0, X_test.loc[selected_row, "lat"])
lon = st.slider("Longitude:", -180.0, 180.0, X_test.loc[selected_row, "lon"])
track = st.slider("Track (degrees):", 0.0, 360.0, X_test.loc[selected_row, "track"])
nac_p = st.slider(
    "Navigation Accuracy Category (Position):",
    0.0,
    10.0,
    X_test.loc[selected_row, "nac_p"],
)
nac_v = st.slider(
    "Navigation Accuracy Category (Velocity):",
    0.0,
    10.0,
    X_test.loc[selected_row, "nac_v"],
)


# User input dictionary to send to the API
user_input = {
    "alt_baro": alt_baro,
    "nav_altitude_mcp": nav_altitude_mcp,
    "lon": lon,
    "gs": gs,
    "geom_rate": geom_rate,
    "lat": lat,
    "track": track,
    "nac_p": nac_p,
    "nac_v": nac_v,
}

# Button to trigger the prediction
if st.button("Predict Category"):
    response = requests.post(
        "http://fastapi_route:8000/airport_predict_adsb",
        json=user_input,
        timeout=15,
    )

    if response.status_code == 200:
        result = response.json()

        # st.write(result)  # Display response for debugging
        print(result)  # Print result in console for verification

        predicted_lat = result.get("predicted_lat", lat)
        predicted_lon = result.get("predicted_lon", lon)
        st.write(
            f"Predicted Latitude: {predicted_lat:.6f}, Predicted Longitude: {predicted_lon:.6f}"
        )

        # Plot the prediction on a map using pydeck
        # #FIXME Change to the uber hex plot Brett gave us (IT WONT WORK)
        st.pydeck_chart(
            pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=predicted_lat,
                    longitude=predicted_lon,
                    zoom=10,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=pd.DataFrame(
                            {"lat": [predicted_lat], "lon": [predicted_lon]}
                        ),
                        get_position="[lon, lat]",
                        get_color="[200, 30, 0, 160]",
                        get_radius=1000,
                    ),
                ],
            )
        )

        # Load the data
        file_path = "fl_airports.csv"  # Update this to your actual file path
        df = pd.read_csv(file_path)

        # Create a base map centered on Florida
        florida_map = folium.Map(
            location=[27.9944024, -81.7602544], zoom_start=6, tiles="cartodbpositron"
        )

        # Add airport markers to the map
        for _, row in df.iterrows():
            # Extract the necessary information
            lat = row["Latitude"]
            lon = row["Longitude"]
            iata = row["IATA"]
            name = row["Name"]

            # Create a marker with a popup showing the IATA code and airport name
            folium.Marker(
                location=[lat, lon],
                popup=f"{iata}: {name}",
                tooltip=iata,
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(florida_map)

        # Display the map in Streamlit
        st.title("Florida Airports Map")
        folium_static(florida_map)

    else:
        st.error(f"Failed to get prediction: {response.status_code}")
        st.write(f"Error details: {response.text}")
