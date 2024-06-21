#!/bin/bash
# This script will give the Compute Service Account GCS Storage Admin permissions so the Cloud Run containers can access storage buckets.
# setup-cloudrun.sh {cloudrun_service_name} {region} {project}
SERVICE=${1:-"gcs-latency-tester"}
REGION=${2:-"us-central1"}
PROJECT=${3:-$(gcloud config get project)}

PROJECT_NUM=$(gcloud projects describe ${PROJECT} --format="value(projectNumber)")

printf "Giving Storage Admin permissions to the Compute SA"

# give the pub/sub invoker SA invoker privs on this new cloud run service
gcloud run services add-iam-policy-binding $SERVICE \
    --member=serviceAccount:$PROJECT_NUM-compute@developer.gserviceaccount.com \
    --role=roles/storage.admin \
    --region=$REGION
