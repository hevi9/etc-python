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

def got_result(future):
  print(future.result())
  loop.stop()

loop = asyncio.get_event_loop()

def main():
  logging.basicConfig(level=logging.DEBUG)
  future = asyncio.Future()
  asyncio.Task(slow_op(future))
  future.add_done_callback(got_result)
  try:
    loop.run_forever()
  finally:  
    loop.close()
  D("done.")


if __name__ == "__main__":
  main()
  