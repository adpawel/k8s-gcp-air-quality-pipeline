import json
from datetime import datetime, timezone

import requests
from google.cloud import storage

URL = (
    "https://air-quality-api.open-meteo.com/v1/air-quality"
    "?latitude=50.06"
    "&longitude=19.94"
    "&current=european_aqi,pm10,pm2_5"
    "&timezone=Europe/Warsaw"
)
BUCKET_NAME = "air-quality-data-lake-pawada-810"


def fetch_air_quality():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()


def upload_to_gcs(bucket_name, source_data, destination_blob_name):
    client = storage.Client(project="de-project-001-503509")
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_string(
        data=json.dumps(source_data), content_type="application/json"
    )
    print(f"Success! File saved in the cloud: gs://{bucket_name}/{destination_blob_name}")
    
    
if __name__ == "__main__":
    print("Fetching air quality data...")
    data = fetch_air_quality()
    
    now = datetime.now(timezone.utc)
    blob_path = f"raw/year={now.year}/month={now.month:02d}/day={now.day:02d}/air_{now.strftime('%H%M%S')}.json"
    
    upload_to_gcs(BUCKET_NAME, data, blob_path)