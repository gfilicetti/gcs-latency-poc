#!/bin/bash
# This script will create a new bucket with the default folders inside
# NOTE: region can be comma delimited list for multi region
# create-storage.sh {bucket_name} {region(s)} {project}
BUCKET=${1:-"gcs-latency-test"}
REGION=${2:-"us-central1"}
PROJECT=${3:-$(gcloud config get project)}

printf "Creating bucking: ${BUCKET} \n"
printf "Using region(s): ${REGION} \n"

# create the new GCS bucket
gsutil mb -l $REGION "gs://${BUCKET}"
