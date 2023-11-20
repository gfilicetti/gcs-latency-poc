#!/bin/bash
# This script will deploy a new cloud run job in the region passed in 
# create-cloudrun-job.sh {cloudrun_job_name} {image} {env_vars} {region} 
JOB=${1:-"gcs-latency-tester"}
ENV=${2:-'LATENCY_TEST_ITERATIONS=10,LATENCY_TEST_FILE_SIZE=5000000,LATENCY_TEST_FILE_PREFIX="file_",LATENCY_TEST_FILE_EXTENSION="ts",LATENCY_TEST_BUCKET_NAME="gcs-latency-test",LATENCY_TEST_FOLDER_NAME="5MB"'}
IMAGE=${3:-"us-central1-docker.pkg.dev/gcs-latency-poc/registry-docker/gcs-latency-tester"}
REGION=${4:-"us-central1"}

printf "Creating cloud run job: ${JOB} \n"
printf "Using environment: ${ENV} \n"
printf "Using image: ${IMAGE} \n"
printf "In region: ${REGION} \n"

# create the new cloud run job
gcloud run jobs create ${JOB} \
    --image ${IMAGE}:latest \
    --region ${REGION} \
    --parallelism=1 \
    --set-env-vars=${ENV} 
