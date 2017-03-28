#!/usr/bin/python3

import fire

class Do:

    def sum(self, *args):
        print(sum(args))

    def add(self, a, b):
        print(a + b)

if __name__ == '__main__':
    fire.Fire(Do)
