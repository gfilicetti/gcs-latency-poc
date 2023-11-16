import random
import os
from argparse import ArgumentParser

def generate_random_data(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def generate_files(num_files, file_size, file_prefix, file_ext):
    for i in range(num_files):
        filename = f"{file_prefix}{i+1}.{file_ext}"
        with open(filename, "w") as f:
            f.write(generate_random_data(file_size))

def main(args):
    num_files = args.num_files
    file_size = args.file_size
    file_prefix = args.file_prefix
    file_ext = args.file_ext
    generate_files(num_files, file_size, file_prefix, file_ext)

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate random files")
    parser.add_argument("--num-files", type=int, help="Number of files to generate", default=10)
    parser.add_argument("--file-size", type=int, help="Size of each file (in bytes)", default=10**6)
    parser.add_argument("--file-prefix", type=str, help="Filename prefix to use", default="file_")
    parser.add_argument("--file-ext", type=str, help="File extension to use", default="txt")

    main(parser.parse_args())
