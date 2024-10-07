"""
Runs with:
uvicorn api_caller:app --reload  
"""

import os
import time
from datetime import datetime, timezone
import requests
import pandas as pd
from dotenv import load_dotenv
import schedule

# Load the environment variables from the .env file
load_dotenv()

# Replace with your actual RapidAPI key
API_KEY = os.getenv("API_KEY")
API_HOST = "adsbexchange-com1.p.rapidapi.com"

# Define the area of interest (e.g., Tampa Bay area coordinates)
LATITUDE = 27.9506
LONGITUDE = -82.4572
DISTANCE = 50  # Radius in nautical miles

# API endpoint template
API_URL_TEMPLATE = "https://{host}/v2/lat/{lat}/lon/{lon}/dist/{dist}/"

# Directory to store data
DATA_DIR = "adsb_data"
os.makedirs(DATA_DIR, exist_ok=True)


def fetch_and_store_data():
    """Construct the API URL"""
    api_url = API_URL_TEMPLATE.format(
        host=API_HOST, lat=LATITUDE, lon=LONGITUDE, dist=DISTANCE
    )

    # Set headers as per API requirements
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    try:
        # Make the API request
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()

        # Parse the ADS-B data
        adsb_data = response.json().get("ac", [])

        if not adsb_data:
            print(f"{datetime.now(timezone.utc)}: No data received.")
            return

        # Convert data to DataFrame
        df = pd.DataFrame(adsb_data)

        # Add a timestamp column
        df["timestamp"] = datetime.now(timezone.utc)

        # Get the number of columns in the DataFrame
        column_count = len(df.columns)

        # Create a unique file name based on the number of columns
        file_name = f"adsb_data_{column_count}_columns.csv"
        file_path = os.path.join(DATA_DIR, file_name)

        # Save to CSV (append if file exists)
        if not os.path.isfile(file_path):
            df.to_csv(file_path, index=False, mode="w", header=True)
        else:
            df.to_csv(file_path, index=False, mode="a", header=False)

        print(
            f"{datetime.now(timezone.utc)}: Data fetched and stored successfully in {file_name}."
        )

    except Exception as e:
        print(f"{datetime.now(timezone.utc)}: An error occurred: {e}")


# Schedule the function to run every 15 minutes
schedule.every(15).minutes.do(fetch_and_store_data)

print("Starting data collection...")

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
