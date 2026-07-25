import json
from datetime import datetime
from google.cloud import bigquery, storage

PROJECT_ID = "de-project-001-503509"
BUCKET_NAME = "air-quality-data-lake-pawada-810"
DATASET_ID = "smog_warehouse"
TABLE_ID = "krakow_air_quality"


def transform_and_load():
    print("Looking for the latest file in the Data Lake (GCS)...")
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)

    blobs = list(bucket.list_blobs(prefix="raw/"))
    if not blobs:
        print("No files in the Data Lake! Run fetching script.")
        return

    latest_blob = max(blobs, key=lambda b: b.time_created)
    print(f"Reading file: {latest_blob.name}")

    raw_content = latest_blob.download_as_text()
    data = json.loads(raw_content)

    current = data.get("current", {})
    row_to_insert = [
        {
            "timestamp": current.get("time", datetime.now().isoformat()),
            "city": "Kraków",
            "european_aqi": current.get("european_aqi"),
            "pm10": current.get("pm10"),
            "pm2_5": current.get("pm2_5"),
            "source_file": latest_blob.name,
        }
    ]

    print("Loading data to BigQuery warehouse...")
    bq_client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    job_config = bigquery.LoadJobConfig(
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=True,
    )

    job = bq_client.load_table_from_json(
        row_to_insert, table_ref, job_config=job_config
    )
    job.result()

    print(f"Success! New row added to the BigQuery table: {table_ref}")


if __name__ == "__main__":
    transform_and_load()