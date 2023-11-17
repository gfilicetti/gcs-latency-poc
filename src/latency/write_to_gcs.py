import sys
import random
import time
import subprocess
import csv
from uuid import uuid4
from argparse import ArgumentParser
from google.cloud import storage
# from tqdm import tqdm

# Constants
BUCKET = "gcs-latency-1"
DIR = "test1"

def generate_random_data(size_in_bytes):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size_in_bytes))

def generate_file(data, file_prefix, file_ext):
    # we only need the 6 least significant digits from the hex of our uuid
    uid = f"{uuid4().hex[-6:]}"
    filename = f"{file_prefix}{uid}.{file_ext}"

    with open(filename, "w") as f:
        f.write(data)

    return filename

def gsutil_file_to_gcs(filename):
    cmd = ["gsutil", "--quiet", "cp", filename, f"gs://{BUCKET}/{DIR}"]
    subprocess.check_call(cmd)

def write_file_to_gcs(filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(f"{DIR}/sdk-{filename}")
    blob.upload_from_filename(filename)

def write_direct_to_gcs(filename, data):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(f"{DIR}/direct-{filename}")

    with blob.open('w') as f:
        f.write(data)

def main(args):

    file_size = args.file_size
    file_prefix = args.file_prefix
    file_ext = args.file_ext
    iterations = args.iterations
    
    writer = csv.writer(sys.stdout)
    writer.writerow(["iteration", "filename", "size_bytes", "time_file_to_gcs", "time_direct_to_gcs"])

    for i in range(iterations):
        data = generate_random_data(file_size)
        filename = generate_file(data, file_prefix, file_ext)

        start = time.perf_counter()
        write_file_to_gcs(filename)
        end = time.perf_counter()
        time_file = int((end - start)*1000%1000)

        start = time.perf_counter()
        write_direct_to_gcs(filename, data)
        end = time.perf_counter()
        time_direct = int((end - start)*1000%1000)

        writer.writerow([i, filename, file_size, time_file, time_direct])
        sys.stdout.flush()

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate random files")
    parser.add_argument("--file-size", type=int, help="Size of each file (in bytes)", default=10**6)
    parser.add_argument("--file-prefix", type=str, help="Filename prefix to use", default="file_")
    parser.add_argument("--file-ext", type=str, help="File extension to use", default="txt")
    parser.add_argument("--iterations", type=int, help="Number of times to run the test", default=5)

    main(parser.parse_args())
