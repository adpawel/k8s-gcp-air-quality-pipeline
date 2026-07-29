from datetime import datetime, timedelta, timezone

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from kubernetes.client import models as k8s

default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "email_on_failure": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    "smog_ingestion_pipeline",
    default_args=default_args,
    description="Pobieranie ze smogu (GCS) -> ETL -> BigQuery",
    schedule="0 * * * *",
    start_date=datetime(2026, 7, 25, tzinfo=timezone.utc),
    catchup=False,
) as dag:

    volume_mount = k8s.V1VolumeMount(
        name="gcp-secret-volume",
        mount_path="/root/.config/gcloud",
        read_only=True,
    )
    volume = k8s.V1Volume(
        name="gcp-secret-volume",
        secret=k8s.V1SecretVolumeSource(secret_name="gcp-credentials"),
    )

    ingest_air_data = KubernetesPodOperator(
        task_id="fetch_and_upload_to_gcs",
        name="air-quality-scraper-pod",
        namespace="airflow",
        image="air-quality-scraper:latest",
        image_pull_policy="Never",
        cmds=["python", "main.py"],
        volumes=[volume],
        volume_mounts=[volume_mount],
        env_vars=[
            k8s.V1EnvVar(
                name="GOOGLE_APPLICATION_CREDENTIALS",
                value="/root/.config/gcloud/key.json",
            )
        ],
        get_logs=False,
        is_delete_operator_pod=False,
    )

    transform_and_load_data = KubernetesPodOperator(
        task_id="transform_json_to_bigquery",
        name="air-quality-etl-pod",
        namespace="airflow",
        image="air-quality-scraper:latest",
        image_pull_policy="Never",
        cmds=["python", "transformator.py"],
        volumes=[volume],
        volume_mounts=[volume_mount],
        env_vars=[
            k8s.V1EnvVar(
                name="GOOGLE_APPLICATION_CREDENTIALS",
                value="/root/.config/gcloud/key.json",
            )
        ],
        get_logs=False,
        is_delete_operator_pod=False,
    )

    ingest_air_data >> transform_and_load_data