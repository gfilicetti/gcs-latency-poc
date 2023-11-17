#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# create-cloudrun.sh {cloudrun_service_name} {region} {image} {project}
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
