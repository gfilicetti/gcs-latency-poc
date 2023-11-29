#!/bin/bash
# This script will execute the passed in cloud run job
# exec-cloudrun-job.sh {cloudrun_job_name} {env_vars} {region}
JOB=${1:-"gcs-latency-tester-murat"}
ENV=${2:-""}
REGION=${3:-"us-central1"}

printf "Executing cloud run job: ${JOB} \n"
printf "With environment: ${ENV} \n"
printf "In region: ${REGION} \n"

# execute the cloud run job
gcloud run jobs execute ${JOB} \
     --region ${REGION} \
     --update-env-vars=${ENV}
