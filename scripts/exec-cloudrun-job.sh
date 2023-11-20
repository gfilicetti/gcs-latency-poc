#!/bin/bash
# This script will execute the passed in cloud run job
# exec-cloudrun-job.sh {cloudrun_job_name} {container_args} {env_vars} {--wait}
JOB=${1:-"gcs-latency-tester"}
ARGS=${2:-""}
REGION=${3:-"us-central1"}

printf "Executing cloud run job: ${JOB} \n"

# execute the cloud run job
gcloud run jobs execute ${JOB} \
     --args=${ARGS} \
     --region ${REGION}
