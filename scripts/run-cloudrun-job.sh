#!/bin/bash
# This script will deploy a new cloud run in the region passed in 
# create-cloudrun.sh {cloudrun_service_name} {region} {image} {project}
SERVICE=${1:-"gcs-latency-tester"}
REGION=${2:-"us-central1"}
IMAGE=${3:-"us-central1-docker.pkg.dev/gcs-latency-poc/registry-docker/gcs-latency-tester"}

printf "Using cloud run service name: ${SERVICE} \n"
printf "Using region: ${REGION} \n"
printf "Using image: ${IMAGE} \n"

# create the new cloud run service
gcloud run jobs create $SERVICE \
    --image=$IMAGE:latest \
    --parallelism=1 \
    --region=$REGION
