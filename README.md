# GCS Latency Proof of Concept
We're going to measure the latency of Google Cloud Storage using small files of various sizes

## File Sizes Used
To mimic file sizes for various segment sizes we're going to use the following:
- 5MB: 3.2s segments
- 9MB: 6.4s segments
- 60MB: 6.4s of 4k segments

## Initial Setup and Bash Scripts
> **Note** There are two versions of some of these scripts, one with no suffix and one with the `murat` suffix. Differences will be noted below

### Create Storage Buckets 

Use this script to create the storage bucket needed, the parameters are optional, if you don't include them we'll use the current project, region: `us-central1` and the name: `gcs-latency-test`

```bash
create-storage.sh <bucket_name> <region> <project>
```

### Setup Cloud Run Permissions

Use this script to give the Compute Service Account GCS Storage Admin permissions so the Cloud Run containers can access storage buckets.

```bash
setup-cloudrun.sh <cloudrun_service_name> <region> <project>
```

## Running The Latency Tests (Locally ONLY)

> **Note** The following bash scripts will test from the local machine only. The Python scripts below are containerized and run in Cloud Run to test latency from Cloud Run in various regions to Google Cloud Storage.

### Deploying a Cloud Run Job

Use this script to deploy a new Cloud Run job in the specified region

```bash
create-cloudrun-job.sh <cloudrun_job_name> <env_vars> <image> <region> 
```

### Executing a Cloud Run Job

Use this script to execute a Cloud Run job that has already been deployed

```bash
exec-cloudrun-job.sh <cloudrun_job_name> <env_vars> <region>
```

## Python Scripts

We have Python scripts that will write to Google Cloud Storage and measure latency as well as a script to generate files of given sizes

### `generate_files.py`

Use this script to generate files with random data inside and deposit them in the current directory:

```bash
python -m latency.generate_files \
    --num-files 10
    --file-size 1000000
    --file-prefix file_
    --file-ext txt
```

### `write_to_gcs.py`

Use this script to test latency of writing to Google Cloud Storage. It will write files of the given size to the given bucket for the number of iterations specified.

```bash
python -m latency.write_to_gcs \
    --iterations 10 \
    --file-size 5000000 \
    --file-prefix file \
    --file-ext ts \
    --bucket-name gcs-latency-test \
    --folder-name 5MB
```

### `write_to_gcs_murat.py`

Use this script achieves the same as `write_to_gcs.py` but it uses files on disk that are already the sizes we want them to be. It has different command line parameters and writes its output to the csv file given instead of stdout.

```bash
python -m latency.write_to_gcs_murat \
    --bucket-name gcs-latency-test \
    --src-file-name 5MB.random \
    --output results.csv \
    --iterations 10
```

## Docker and Google Cloud Build

### `Dockerfile`

The Dockerfile is used to build the container that will be run by Cloud Run. It will run the `write_to_gcs.py` Python script.

It requires certain environment variables that are used as defaults when running the Python scripts, these include:

- `LATENCY_TEST_ITERATIONS`: 10
- `LATENCY_TEST_FILE_SIZE`: 5000000
- `LATENCY_TEST_FILE_PREFIX`: "file"
- `LATENCY_TEST_FILE_EXTENSION`: "ts"
- `LATENCY_TEST_BUCKET_NAME`: "gcs-latency-test"
- `LATENCY_TEST_FOLDER_NAME`: "5MB"

### `Dockerfile-murat`

This Dockerfile is for running the `write_to_gcs_murat.py` Python script. 

It requires different environment variables:

- `LATENCY_TEST_ITERATIONS`: 10
- `LATENCY_TEST_BUCKET_NAME`: "gcs-latency-murat"
- `LATENCY_TEST_SRC_FILE`: "5MB.random"

### `cloudbuild.yaml`

This configuration file for Cloud Build will build a container using `Dockerfile` and push it to Artifact Registry (registry name is hardcoded inside).

### `cloudbuild-murat.yaml`

This configuration file for Cloud Build will build a container using `Dockerfile-murat` and push it to Artifact Registry (registry name is hardcoded inside).