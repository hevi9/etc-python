#!/usr/bin/env python3
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-task.html

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio

@asyncio.coroutine
def slow_op(future):
  yield from asyncio.sleep(1)
  future.set_result("Future is done")


def main():
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  future = asyncio.Future()
  asyncio.Task(slow_op(future))
  loop.run_until_complete(future)
  print(future.result())
  loop.close()
  D("done.")


if __name__ == "__main__":
  main()
  