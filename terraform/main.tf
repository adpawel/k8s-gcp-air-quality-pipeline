terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "de-project-001-503509"
  region  = "europe-central2"
}

resource "google_storage_bucket" "data_lake" {
  name          = "air-quality-data-lake-pawada-810"
  location      = "EUROPE-CENTRAL2"
  
  force_destroy = true 
}

resource "google_bigquery_dataset" "air_quality_dwh" {
  dataset_id                 = "smog_warehouse"
  friendly_name              = "Krakow air quality warehouse"
  description                = "Table with processed data from open API"
  location                   = "EUROPE-CENTRAL2"
  delete_contents_on_destroy = true
}