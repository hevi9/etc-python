#!/usr/bin/env python3.4
## -*- coding: utf-8 -*-

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio # http://docs.python.org/3.4/library/asyncio.html
from simeb import broker

@asyncio.coroutine
def start():
  yield from asyncio.sleep(1)
  D("start")

@asyncio.coroutine
def start2():
  yield from asyncio.sleep(2)
  D("start2")


def main():
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  asyncio.Task(start())
  asyncio.Task(start2())
  loop.run_forever()
  D("done.")


if __name__ == "__main__":
  main()
  