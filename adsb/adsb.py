"""Runs with http://127.0.0.1:8000/get_adsb_data?latitude=27.943721&longitude=-82.537932&radius=5"""

import csv
import sys
import requests
import io
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI()

API_KEY = "25649f62f2msh3808137a2442080p186039jsn6c56c32c82f1"  # Replace with your actual API key
API_HOST = "adsbexchange-com1.p.rapidapi.com"
API_URL_TEMPLATE = "/v2/lat/{lat}/lon/{lon}/dist/{dist}/"


@app.get("/get_adsb_data")
def get_adsb_data(latitude: float, longitude: float, radius: int):
    """
    Queries ADS-B data within a specified radius and returns the results as a CSV file.
    """

    # Construct the full API URL
    api_url = f"https://{API_HOST}" + API_URL_TEMPLATE.format(
        lat=latitude, lon=longitude, dist=radius
    )

    # Set headers as per API requirements
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST,
    }

    try:
        # Make the API request
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        # Parse the ADS-B data
        adsb_data = response.json().get("ac", [])

        # Collect all field names from the data in order
        fieldnames = []
        for entry in adsb_data:
            for key in entry.keys():
                if key not in fieldnames:
                    fieldnames.append(key)

        # Create CSV output
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for entry in adsb_data:
            writer.writerow({field: entry.get(field, "") for field in fieldnames})

        # Return the CSV data as a streaming response
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=adsb_data.csv"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
