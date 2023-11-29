import argparse
import io
import os
import time
from uuid import uuid4

import pandas as pd
from google.cloud import storage


def read(filename: str) -> bytes:
    with open(filename, "rb") as f:
        return f.read()


def blob_write(bucket_name: str, data: bytes, n: int) -> list[float]:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    times = [0.0] * n
    for i in range(n):
        name = uuid4().hex
        blob = bucket.blob(name)
        start = time.perf_counter()
        with blob.open("wb") as f:
            f.write(data)
        times[i] = time.perf_counter() - start
    return times


def upload_from_string(bucket_name: str, data: bytes, n: int) -> list[float]:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    times = [0.0] * n
    for i in range(n):
        name = uuid4().hex
        blob = bucket.blob(name)
        start = time.perf_counter()
        blob.upload_from_string(data)
        times[i] = time.perf_counter() - start
    return times


def upload_from_filename(bucket_name: str, src_file_name: str, n: int) -> list[float]:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    times = [0.0] * n
    for i in range(n):
        name = uuid4().hex
        blob = bucket.blob(name)
        start = time.perf_counter()
        blob.upload_from_filename(src_file_name)
        times[i] = time.perf_counter() - start
    return times


def upload_from_file(bucket_name: str, data: bytes, n: int) -> list[float]:
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    file_obj = io.BytesIO(data)
    times = [0.0] * n
    for i in range(n):
        name = uuid4().hex
        blob = bucket.blob(name)
        start = time.perf_counter()
        file_obj.seek(0)
        blob.upload_from_file(file_obj)
        times[i] = time.perf_counter() - start
    return times


def process(args):
    data = read(args.src_file_name)
    t_s = upload_from_string(args.bucket_name, data, args.iterations)
    t_f = upload_from_file(args.bucket_name, data, args.iterations)
    t_n = upload_from_filename(args.bucket_name, args.src_file_name, args.iterations)
    t_w = blob_write(args.bucket_name, data, args.iterations)

    with open(args.output, "w") as f:
        f.write("from_string, from_file, from_file_name, blob_write\n")
        rows = zip(t_s, t_f, t_n, t_w)
        for row in rows:
            line = ",".join(map(str, row))
            f.write(f"{line}\n")


def summary(output_file_name: str):
    df = pd.read_csv(output_file_name)
    print(df.describe())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket-name", default=os.getenv("LATENCY_TEST_BUCKET_NAME", "meken-playground-blobs"))
    parser.add_argument("--src-file-name", default=os.getenv("LATENCY_TEST_SRC_FILE", "random.bytes"))
    parser.add_argument("--output", default=os.getenv("LATENCY_TEST_OUTPUT_FILE", "results.csv"))
    parser.add_argument("--iterations", type=int, nargs="?", default=os.getenv("LATENCY_TEST_ITERATIONS", 10))

    args = parser.parse_args()

    process(args)
    summary(args.output)
