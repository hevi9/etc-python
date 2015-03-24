#!/usr/bin/env python3
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-task.html

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio

@asyncio.coroutine
def compute(x, y):
  print("compute %s + %s .." % (x,y))
  yield from asyncio.sleep(1)
  return x + y

@asyncio.coroutine
def print_sum(x, y):
  result = yield from compute(x, y)
  print("%s + %s = %s" % (x,y,result))


def main():
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(print_sum(1,2))
  loop.close()
  D("done.")


if __name__ == "__main__":
  main()
  