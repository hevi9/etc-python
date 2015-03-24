#!/usr/bin/env python3
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-task.html#asyncio-hello-world-coroutine

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio # http://docs.python.org/3.4/library/asyncio.html

@asyncio.coroutine
def print_and_repeat():
  while True:
    print("Hello")
    yield from asyncio.sleep(1)

def main():
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(print_and_repeat())
  D("done.")


if __name__ == "__main__":
  main()
  