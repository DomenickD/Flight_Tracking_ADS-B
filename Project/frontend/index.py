"""The entry point file for the streamlit app"""

import streamlit as st

st.title("Welcome to the ADS-B Data Brief")
st.write("By: Domenick Dobbs")

st.divider()

st.subheader("The Project Thesis")

st.write(
    """
The objective of this project is to analyze ADS-B (Automatic Dependent Surveillance-Broadcast) 
data to uncover insights related to aircraft movements. ADS-B data provides real-time 
information about an aircraft's position, altitude, speed, and other critical parameters. 
Through machine learning models, we aim to predict aircraft behavior and classify flight 
types. The goal is to build predictive models that can assist in air traffic analysis and monitoring.
"""
)

st.divider()

st.subheader("About the Data")

st.write(
    """
    The ADS-B data contains information on various aircraft parameters, including but not limited to:
    - **Altitude (alt_baro and alt_geom)**: Measures the altitude of the aircraft.
    - **Ground Speed (gs)**: The speed of the aircraft relative to the ground.
    - **Latitude and Longitude (lat and lon)**: Coordinates of the aircraft at a given time.
    - **Aircraft Category (category)**: Classification of the aircraft type, such as commercial, private, or military.
    - **Flight Identifier (flight)**: Unique identification code for the flight.
    - **Emergency and Alert Status (emergency and alert)**: Flags indicating whether the aircraft is experiencing an emergency.

    The dataset has been cleaned, missing values have been handled, and categorical features like 'category' have been encoded 
    to make them suitable for machine learning models.
"""
)

st.divider()

st.subheader("About the Model")

st.write(
    """
The machine learning models explored in this project included Random Forest, SVC (Support Vector Classifier), 
Logistic Regression, and Neural Networks, with the goal of predicting various aircraft behaviors, 
such as flight type classification and detecting potential anomalies in flight patterns.  

After evaluating these models and performing hyperparameter tuning using RandomizedSearchCV, 
the Random Forest model consistently demonstrated the best performance.  
Therefore, we'll focus on showcasing the results and capabilities of the Random Forest model in this project.

The Tuned Random Forest Test Accuracy is 97.11%.
"""
)

st.divider()

st.subheader("What to expect in this presentation")

st.write(
    """
In this presentation, we will cover:
    1. **Data Exploration**: A breakdown of the ADS-B data, including visualizations of key features such as altitude, speed, and aircraft category.
    2. **Model Training**: A demonstration of the machine learning models used, including hyperparameter tuning and model evaluation.
    3. **Model Performance**: Evaluation metrics such as accuracy, precision, recall, and F1-score for each model will be presented.
    4. **Prediction Use Cases**: Examples of predictions from the models, including classification of aircraft types and detection of flight anomalies.
    5. **Conclusions and Future Work**: Summary of the project results and a look at potential next steps, including enhancing the model to detect emergency situations in real-time.
    
"""
)

st.divider()
