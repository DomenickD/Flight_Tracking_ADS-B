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
    
| **Column Name**   | **Description**                                                                                | **Data Type** | **Example Value** |
|-------------------|------------------------------------------------------------------------------------------------|-------------- |------------------ |
| `alt_baro`        | Barometric altitude of the aircraft, measured in feet.                                          | Float          | 35000.0            |
| `flight`          | The flight identifier or flight number assigned to the aircraft.                                | String         | "AA1234"           |
| `nav_altitude_mcp`| The altitude set in the aircraft's Mode Control Panel (MCP), measured in feet.                  | Float          | 30000.0            |
| `emergency`       | Indicator for emergency status (e.g., 0 = none, 1 = emergency declared).                        | Integer        | 0                  |
| `lon`             | Longitude of the aircraft's position, measured in decimal degrees.                              | Float          | -80.0851           |
| `alert`           | Alert status indicator (e.g., 0 = no alert, 1 = alert triggered).                               | Integer        | 0                  |
| `baro_rate`       | Rate of climb or descent based on barometric altitude, measured in feet per minute.             | Float          | 1500.0             |
| `gs`              | Ground speed of the aircraft, measured in knots.                                                | Float          | 450.0              |
| `geom_rate`       | Geometric rate of climb or descent, measured in feet per minute.                                | Float          | -500.0             |
| `hex`             | The ICAO 24-bit address of the aircraft, usually represented as a hexadecimal string.           | String         | "ABC123"           |
| `lat`             | Latitude of the aircraft's position, measured in decimal degrees.                               | Float          | 25.7617            |
| `alt_geom`        | Geometric altitude of the aircraft, measured in feet.                                           | Float          | 34500.0            |
| `track`           | Aircraft's ground track angle, measured in degrees from true north (0-360).                     | Float          | 180.0              |
| `t`               | Aircraft type or model (if available, often provided as a code).                                | String         | "B738"             |
| `nac_p`           | Navigation Accuracy Category for Position, indicating the accuracy of the position measurement. | Integer        | 8                  |
| `nac_v`           | Navigation Accuracy Category for Velocity, indicating the accuracy of the velocity measurement. | Integer        | 2                  |
| `category`        | Emitter category of the aircraft, providing general information about its weight or type.       | String         | "A3"               |


    The dataset has been cleaned, missing values have been handled, and categorical features like 'category' have been encoded 
    to make them suitable for machine learning models.
    Note: A flaw was found when plotting Lat and Long.
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
