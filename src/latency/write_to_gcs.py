import sys
import time
import random
import csv

from uuid import uuid4
from argparse import ArgumentParser

from google.cloud import storage

def generate_random_data(size_in_bytes):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size_in_bytes))

def generate_file(data, file_prefix, file_ext):
    # we only need the 6 least significant digits from the hex of our uuid
    uid = f"{uuid4().hex[-6:]}"
    filename = f"{file_prefix}{uid}.{file_ext}"

    with open(filename, "w") as f:
        f.write(data)

    return filename

def write_file_to_gcs(bucket, folder, filename):
    blob = bucket.blob(f"{folder}/sdk-{filename}")
    blob.upload_from_filename(filename)

def write_direct_to_gcs(bucket, folder, filename, data):
    blob = bucket.blob(f"{folder}/direct-{filename}")

    with blob.open('w') as f:
        f.write(data)

def main(args):

    iterations = args.iterations
    file_size = args.file_size
    file_prefix = args.file_prefix
    file_ext = args.file_ext
    bucket_name = args.bucket_name
    folder_name = args.folder_name
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    writer = csv.writer(sys.stdout)
    writer.writerow(["iteration", "filename", "size_mb", "time_file_to_gcs", "time_direct_to_gcs"])

    for i in range(iterations):
        data = generate_random_data(file_size)
        filename = generate_file(data, file_prefix, file_ext)

        start = time.perf_counter()
        write_file_to_gcs(bucket, folder_name, filename)
        end = time.perf_counter()
        time_file = int((end - start)*1000%1000)

        start = time.perf_counter()
        write_direct_to_gcs(bucket, folder_name, filename, data)
        end = time.perf_counter()
        time_direct = int((end - start)*1000%1000)

        writer.writerow([i, filename, int(file_size/10**6), time_file, time_direct])
        sys.stdout.flush()

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate random files")
    parser.add_argument("--iterations", type=int, help="Number of times to run the test", default=10)
    parser.add_argument("--file-size", type=int, help="Size of each file (in bytes)", default=5*(10**6))
    parser.add_argument("--file-prefix", type=str, help="Filename prefix to use", default="file_")
    parser.add_argument("--file-ext", type=str, help="File extension to use", default="ts")
    parser.add_argument("--bucket-name", type=str, help="Name of GCS Bucket", default="gcs-latency-test")
    parser.add_argument("--folder-name", type=str, help="Folder in bucket to use", default="5MB")

    main(parser.parse_args())
