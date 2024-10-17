"""Handles all backend logic"""

import sqlite3
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder

# Initialize FastAPI app
app = FastAPI()

label_encoder = LabelEncoder()

# Load the pre-trained models from pickle files
with open(r"models/adsb_rf_model.pkl", "rb") as model_file:
    best_rf_model = pickle.load(model_file)

with open(r"models/adsb_scaler.pkl", "rb") as model_file:
    scaler = pickle.load(model_file)

with open(r"models/adsb_le.pkl", "rb") as model_file:
    le = pickle.load(model_file)


# Connect to the SQLite3 database FIXME
DATABASE = "adsb_data.db"


# The SQLITE DB query
def query_database(query_intake):
    """
    This is the function to do the actual database querying.
    """
    conn = sqlite3.connect("/app/adsb_data.db")  # Adjust path if needed
    cursor = conn.cursor()
    cursor.execute(query_intake)
    columns = [description[0] for description in cursor.description]  # Get column names
    data = cursor.fetchall()
    conn.close()
    return {"columns": columns, "data": data}


# Route to test the API
@app.get("/")
async def root():
    """FIXME do I need this?"""
    return {"message": "Welcome to the ADS-B backend API"}


# Route to handle ADS-B category predictions
@app.post("/predict_adsb_category")
async def predict_adsb_category(request: Request):
    """
    This function takes in an array of data and uses it to
    predict the ADS-B category against a pretrained model.
    """
    try:
        columns_order = [
            "lon",
            "emergency",
            "flight",
            "nac_p",
            "gs",
            "t",
            "alert",
            "baro_rate",
            "alt_baro",
            "track",
            "hex",
            "alt_geom",
            "lat",
            "geom_rate",
            "nav_altitude_mcp",
            "nac_v",
        ]
        # Get the JSON data from the request
        json_data = await request.json()
        df = pd.DataFrame([json_data], columns=columns_order)

        print(df)
        # Scale the data
        scaled_data = scaler.transform(df)

        # Perform prediction
        prediction = best_rf_model.predict(scaled_data)[0]

        category = le.inverse_transform([prediction])[0]
        print(category)
        return {"category": category}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")


@app.post("/query")
async def query_route(request: Request):
    """
    This function handles SQL queries for the database file in another Docker container.
    """
    try:
        request_data = await request.json()  # Get the JSON data from the request body
        query = request_data.get("query")  # Extract the query from the JSON

        if not query:
            raise HTTPException(status_code=400, detail="No query provided")

        # Query the database
        data = query_database(query)
        return {"data": data}

    except sqlite3.DatabaseError as db_error:
        raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")

    # except ValueError as val_error:
    #     raise HTTPException(status_code=400, detail=f"Value error: {str(val_error)}")

    # except KeyError as key_error:
    #     raise HTTPException(status_code=400, detail=f"KeyError: {str(key_error)}")

    # except IOError as io_error:
    #     raise HTTPException(status_code=500, detail=f"IOError: {str(io_error)}")
