#!/bin/bash
# This script will execute the passed in cloud run job
# exec-cloudrun-job.sh {cloudrun_job_name} {container_args} {env_vars} {--wait}
JOB=${1:-"gcs-latency-tester"}
ARGS=${2:-"arg1,arg2,arg3"}
ENV_VARS=${3:-"VAR1=VAL1,VAR2=VAL2"}
REGION=${4:-"us-central1"}

printf "Executing cloud run job: ${JOB} \n"

# execute the cloud run job
gcloud run jobs execute ${JOB} \
     --args ${ARGS} \
     --update-env-vars ${ENV_VARS} \
     --region ${REGION}