#!/usr/bin/python3
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from getpass import getuser
from math import floor, log

import time

ARGS = ArgumentParser()
ARGS.add_argument("--create",
                  type=int,
                  help="create test file, size in Megabytes")
ARGS.add_argument("--bench",
                  action="store_true",
                  help="benchmark")

file_path = Path("/tmp", getuser(), "readvvsread.bin")


def bytes(b):
    """ Formats number of bytes into human readable 2-based format.
    b as int is amount of bytes. Return text as str."""
    if b == 0:
        return "0B"
    n = floor(log(b, 2) / 10)
    u = "kMGTPEZY"[n - 1] if n else ""
    f = str(b / (pow(2, n * 10)))
    f = f[:4] if len(f) > 4 else f
    f = f.rstrip(".")
    return "{}{}B".format(f, u)


def create_test_file(file_size):
    block_size = 13 * (2 ** 10)
    block_data = b'A' * block_size
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(file_path), 'wb') as fo:
        data_wrote = 0
        while data_wrote < file_size:
            bytes = fo.write(
                block_data[0:min(block_size, file_size - data_wrote)])
            data_wrote += bytes
    print("created {}, size={}B".format(file_path, file_size))


def bench_read():
    """ read """
    block_size = 8 * 2 ** 10
    read_size = 0
    with open(str(file_path), 'rb') as fo:
        data = fo.read(block_size)
        read_size += len(data)
        while data:
            data = fo.read(block_size)
            read_size += len(data)
    return read_size

def bench_readv():
    """ readv """



def bench_time(fn, loops = 100):
    times = []
    for _ in range(loops):
        time_start = time.process_time()
        read_size = fn()
        times.append((time.process_time() - time_start, read_size))
    # report
    name = fn.__doc__.strip()
    avg_time = sum([i[0] for i in times]) / loops
    avg_size = sum([i[1] for i in times]) / loops
    rate = bytes(int(avg_size / avg_time))
    avg_size = bytes(avg_size)
    summary = "{name} {avg_time}s {avg_size} {rate}/s".format(**vars())
    print(summary)


def main(argv=sys.argv[1:]):
    args = ARGS.parse_args(argv)
    if args.create:
        create_test_file(args.create * 2 ** 20)
    elif args.bench:
        bench_time(bench_read)
    else:
        ARGS.print_help()


if __name__ == "__main__":
    main()
