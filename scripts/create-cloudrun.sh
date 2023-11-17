#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# create-cloudrun.sh {cloudrun_service_name} {region} {image} {project}
SERVICE=${1:-"gcs-latency-tester"}
REGION=${2:-"us-central1"}
IMAGE=${3:-"us-central1-docker.pkg.dev/gcs-latency-poc/registry-docker/gcs-latency-tester"}
PROJECT=${4:-$(gcloud config get project)}
PROJECT_NUM=$(gcloud projects describe ${PROJECT} --format="value(projectNumber)")

printf "Using cloud run service name: ${SERVICE} \n"
printf "Using region: ${REGION} \n"
printf "Using image: ${IMAGE} \n"
printf "Using project: ${PROJECT} \n"

# create the new cloud run service
gcloud run deploy $SERVICE \
    --image=$IMAGE:latest \
    --min-instances=1 \
    --no-cpu-throttling \
    --allow-unauthenticated \
    --cpu-boost \
    --region=$REGION

# give the pub/sub invoker SA invoker privs on this new cloud run service
gcloud run services add-iam-policy-binding $SERVICE \
    --member=serviceAccount:$PROJECT_NUM-compute@developer.gserviceaccount.com \
    --role=roles/storage.admin \
    --region=$REGION
