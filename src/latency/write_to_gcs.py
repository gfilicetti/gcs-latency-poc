import os
import io
import sys
import time
import random
import csv
import datetime

from uuid import uuid4
from argparse import ArgumentParser

import pandas as pd
from pydoc import describe
from tqdm import tqdm
from google.cloud import storage

def generate_random_data(size_in_bytes):
    data_string = ''.join(chr(random.randint(65, 90)) for _ in range(size_in_bytes))
    bytes = data_string.encode('utf-8')
    return bytes

def generate_file(data, file_prefix, file_ext):
    # we only need the 6 least significant digits from the hex of our uuid
    uid = f"{uuid4().hex[-6:]}"
    filename = f"{uid}-{file_prefix}.{file_ext}"

    with open(filename, "wb") as f:
        f.write(data)

    return filename

def write_file_to_gcs(bucket, folder, filename, data):
    blob = bucket.blob(f"{folder}/by-file-{filename}")
    file_obj = io.BytesIO(data)
    file_obj.seek(0)
    start = time.perf_counter()
    blob.upload_from_file(file_obj)
    return time.perf_counter() - start

def write_filename_to_gcs(bucket, folder, filename):
    blob = bucket.blob(f"{folder}/by-filename-{filename}")
    start = time.perf_counter()
    blob.upload_from_filename(filename)
    return time.perf_counter() - start

def write_string_to_gcs(bucket, folder, filename, data):
    blob = bucket.blob(f"{folder}/by-string-{filename}")
    start = time.perf_counter()
    blob.upload_from_string(data)
    return time.perf_counter() - start

def write_direct_to_gcs(bucket, folder, filename, data):
    blob = bucket.blob(f"{folder}/by-stream-{filename}")

    start = time.perf_counter()

    with blob.open('wb') as f:
        f.write(data)

    return time.perf_counter() - start

def output_results(test_results, bucket, folder, file_prefix):
    headers = ["time_file", "time_filename", "time_string", "time_direct"]
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H_%M")

    # Write results into blob storage
    blob = bucket.blob(f"{folder}/results-{file_prefix}-{timestamp}.csv")

    blob_file = csv.writer(blob.open('w'))
    blob_file.writerow(headers)
    blob_file.writerows(test_results)

    # Write results to stdout
    stdout = csv.writer(sys.stdout)
    stdout.writerow(headers)
    stdout.writerows(test_results)

    # Use panda to get stats 
    df = pd.DataFrame(test_results, columns=["time_file", "time_filename", "time_string", "time_direct"])
    stats = str(df.describe())

    # Output stats to GCS and to stdout
    blob = bucket.blob(f"{folder}/results-{file_prefix}-{timestamp}-stats.txt")
    with blob.open('w') as f:
        f.write(stats)

    print(stats)

def main(args):
    iterations = args.iterations
    file_size = args.file_size
    file_prefix = args.file_prefix
    file_ext = args.file_ext
    bucket_name = args.bucket_name
    folder_name = args.folder_name
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    test_results = [0] * iterations

    for i in tqdm(range(iterations), desc="Testing GCS Latency", unit="Test", colour="green"):
        data = generate_random_data(file_size)
        filename = generate_file(data, file_prefix, file_ext)

        time_file = write_file_to_gcs(bucket, folder_name, filename, data)
        time_filename = write_filename_to_gcs(bucket, folder_name, filename)
        time_string = write_string_to_gcs(bucket, folder_name, filename, data)
        time_direct = write_direct_to_gcs(bucket, folder_name, filename, data)

        test_results[i] = (time_file, time_filename, time_string, time_direct)

    output_results(test_results, bucket, folder_name, file_prefix)


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate random files")
    parser.add_argument("--iterations", type=int, help="Number of times to run the test", default=os.getenv("LATENCY_TEST_ITERATIONS", 10))
    parser.add_argument("--file-size", type=int, help="Size of each file (in bytes)", default=os.getenv("LATENCY_TEST_FILE_SIZE", 5*(10**6)))
    parser.add_argument("--file-prefix", type=str, help="Filename prefix to use", default=os.getenv("LATENCY_TEST_FILE_PREFIX", "file"))
    parser.add_argument("--file-ext", type=str, help="File extension to use", default=os.getenv("LATENCY_TEST_FILE_EXTENSION", "ts"))
    parser.add_argument("--bucket-name", type=str, help="Name of GCS Bucket", default=os.getenv("LATENCY_TEST_BUCKET_NAME", "gcs-latency-test"))
    parser.add_argument("--folder-name", type=str, help="Folder in bucket to use", default=os.getenv("LATENCY_TEST_FOLDER_NAME", "5MB"))

    main(parser.parse_args())

