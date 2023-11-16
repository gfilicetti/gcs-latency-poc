import random
import time
import subprocess
from uuid import uuid4
from argparse import ArgumentParser
from google.cloud import storage

# Constants
BUCKET = "gcs-latency-1"
DIR = "test1"

def generate_random_data(size_in_bytes):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size_in_bytes))

def generate_file(file_size, file_prefix, file_ext):
    # we only need the 6 least significant digits from the hex of our uuid
    uid = f"{uuid4().hex[-6:]}"
    filename = f"{file_prefix}{uid}.{file_ext}"

    with open(filename, "w") as f:
        f.write(generate_random_data(file_size))

    return filename

def gcs_write_with_gsutil(filename):
    cmd = ["gsutil", "--quiet", "cp", filename, f"gs://{BUCKET}/{DIR}"]

    subprocess.check_call(cmd)

def gcs_write_with_sdk(filename):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(f"{DIR}/{filename}")
    blob.upload_from_filename(filename)

def gcs_write_direct():
    return

def main(args):
    file_size = args.file_size
    file_prefix = args.file_prefix
    file_ext = args.file_ext

    start = time.perf_counter()
    filename = generate_file(file_size, file_prefix, file_ext)
    end = time.perf_counter()
    print(f"Write to disk: {int((end - start)*1000%1000)}ms")

    # start = time.perf_counter()
    # gcs_write_with_gsutil(filename)
    # end = time.perf_counter()
    # print(f"Write disk to GCS (gsutil): {int((end - start)*1000%1000)}ms")

    start = time.perf_counter()
    gcs_write_with_sdk(filename)
    end = time.perf_counter()
    print(f"Write disk to GCS (SDK): {int((end - start)*1000%1000)}ms")

    # start = time.perf_counter()
    # gcs_write_direct()
    # end = time.perf_counter()
    # print(f"Write Direct to GCS (SDK): {int((end - start)*1000%1000)}ms")

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate random files")
    parser.add_argument("--file-size", type=int, help="Size of each file (in bytes)", default=10**6)
    parser.add_argument("--file-prefix", type=str, help="Filename prefix to use", default="file_")
    parser.add_argument("--file-ext", type=str, help="File extension to use", default="txt")

    main(parser.parse_args())
