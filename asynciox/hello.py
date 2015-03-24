#!/usr/bin/env python3
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-eventloop.html

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio # http://docs.python.org/3.4/library/asyncio.html


def print_and_repeat(loop):
  print("Hello")
  loop.call_later(2, print_and_repeat, loop)

def main():
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  loop.call_soon(print_and_repeat, loop)
  loop.run_forever()
  D("done.")


if __name__ == "__main__":
  main()
  