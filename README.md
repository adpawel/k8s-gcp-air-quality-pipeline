# 🌩️ Cloud & Kubernetes Air Quality ETL Pipeline

An automated Data Engineering pipeline deployed on **Kubernetes (Kind)** using **Apache Airflow 3** and **Google Cloud Platform (GCP)**. It fetches real-time air pollution data for Kraków (PM10, PM2.5, AQI) from the Open-Meteo API, stores raw JSON in **Google Cloud Storage (Data Lake)**, transforms the data using **Python**, and loads relational analytical tables into **Google BigQuery (Data Warehouse)**.

## 🏗️ Architecture

```mermaid
graph TD
    API[Open-Meteo Air Quality API] -->|JSON Ingestion| K8S_POD_1[K8s Pod: Ingestion Task]
    K8S_POD_1 -->|Partitions: raw/year/month/day/| GCS[(Google Cloud Storage Data Lake)]
    GCS -->|Raw JSON| K8S_POD_2[K8s Pod: ETL Transform Task]
    K8S_POD_2 -->|Clean Relational Data| BQ[(Google BigQuery Data Warehouse)]

    subgraph K8S [Kubernetes Cluster / Kind]
        AIRFLOW[Apache Airflow 3 Scheduler] -->|KubernetesPodOperator| K8S_POD_1
        AIRFLOW -->|KubernetesPodOperator| K8S_POD_2
    end
```

## 🛠️ Tech Stack

- **Cloud Platform:** Google Cloud Platform (GCS Data Lake, BigQuery Data Warehouse)
- **Infrastructure as Code (IaC):** Terraform
- **Containerization & Orchestration:** Docker, Kubernetes (Kind), Helm Charts
- **Workflow Management:** Apache Airflow 3 (KubernetesPodOperator, LocalExecutor)
- **Language & Libraries:** Python 3.10, google-cloud-storage, google-cloud-bigquery

## 🚀 Key Engineering Achievements

- Resolved Kubernetes ephemeral storage constraints and DNS resolution limits in isolated Airflow workers.
- Implemented secure IAM role and credential passing via Kubernetes Secrets (`V1SecretVolumeSource`).
- Automated table schema evolution in BigQuery with `ALLOW_FIELD_ADDITION`.


## 📊 Pipeline Results


### 1. Airflow DAG Execution (KubernetesPodOperator)
<img width="1902" height="912" alt="obraz" src="https://github.com/user-attachments/assets/fdd5038e-81f3-461c-8b57-42ff048bddcb" />


### 2. BigQuery Data Warehouse Table
<img width="1910" height="798" alt="obraz" src="https://github.com/user-attachments/assets/c2fe23fc-c589-4582-803d-d7ba28dd4a29" />


https://datastudio.google.com/reporting/6198380d-531c-417c-a8f5-66cae642bbdc


