#!/usr/bin/python3
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
from getpass import getuser
from timeit import  timeit

ARGS = ArgumentParser()
ARGS.add_argument("--create",
                  type=int,
                  help="create test file, size in Megabytes")
ARGS.add_argument("--bench",
                  action="store_true",
                  help="benchmark")

file_path = Path("/tmp",getuser(),"readvvsread.bin")

def create_test_file(file_size):
    block_size = 13*(2**10)
    block_data = b'A' * block_size
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(file_path),'wb') as fo:
        data_wrote = 0
        while data_wrote < file_size:
            bytes = fo.write(block_data[0:min(block_size, file_size - data_wrote)])
            data_wrote += bytes
    print("created {}, size={}B".format(file_path, file_size))


def bench_read():
    with open(str(file_path), 'rb') as fo:
        data = fo.read(8 * 2 ** 10)
        while data:
            data = fo.read(8*2**10)

def main(argv=sys.argv[1:]):
    args = ARGS.parse_args(argv)
    if args.create:
        create_test_file(args.create * 2 ** 20)
    elif args.bench:
        loops = 10
        time = timeit('bench_read()', number=loops, globals=globals())
        print("read {time}".format(**vars()))
    else:
        ARGS.print_help()


if __name__ == "__main__":
    main()
