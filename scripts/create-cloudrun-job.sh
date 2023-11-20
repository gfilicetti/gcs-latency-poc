#!/bin/bash
# This script will deploy a new cloud run job in the region passed in 
# create-cloudrun-job.sh {cloudrun_job_name} {image} {arguments} {region} 
JOB=${1:-"gcs-latency-tester"}
ARGS=${2:-"-m,latency.write_to_gcs,10,5000000,file_,ts,gcs_latency_test,5MB"}
IMAGE=${3:-"us-central1-docker.pkg.dev/gcs-latency-poc/registry-docker/gcs-latency-tester"}
REGION=${4:-"us-central1"}

printf "Creating cloud run job: ${JOB} \n"
printf "Using image: ${IMAGE} \n"
printf "Using args: ${ARGS} \n"
printf "Using region: ${REGION} \n"

# create the new cloud run job
gcloud run jobs create ${JOB} \
    --image ${IMAGE}:latest \
    --command "python" \ 
    --args ${ARGS}" \
    --parallelism 1 \
    --region ${REGION}
