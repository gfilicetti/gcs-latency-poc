#!/bin/bash
# This script will deploy a new cloud run job in the region passed in 
# create-cloudrun-job.sh {cloudrun_job_name} {region} {image}
JOB=${1:-"gcs-latency-tester"}
REGION=${2:-"us-central1"}
IMAGE=${3:-"us-central1-docker.pkg.dev/gcs-latency-poc/registry-docker/gcs-latency-tester"}

printf "Creating cloud run job: ${JOB} \n"
printf "Using region: ${REGION} \n"
printf "Using image: ${IMAGE} \n"

# create the new cloud run job
gcloud run jobs create $JOB \
    --image=$IMAGE:latest \
    --parallelism=1 \
    --region=$REGION
