#!/bin/bash
# This script will execute the passed in cloud run job
# exec-cloudrun-job.sh {cloudrun_job_name} {env_vars} {region}
JOB=${1:-"gcs-latency-tester"}
ENV=${2:-'LATENCY_TEST_ITERATIONS=10,LATENCY_TEST_FILE_SIZE=5000000,LATENCY_TEST_FILE_PREFIX="file_",LATENCY_TEST_FILE_EXTENSION="ts",LATENCY_TEST_BUCKET_NAME="gcs-latency-test",LATENCY_TEST_FOLDER_NAME="5MB"'}
REGION=${3:-"us-central1"}

printf "Executing cloud run job: ${JOB} \n"
printf "With environment: ${ENV} \n"
printf "In region: ${REGION} \n"

# execute the cloud run job
gcloud run jobs execute ${JOB} \
     --update-env-vars=${ENV} \
     --region ${REGION}
