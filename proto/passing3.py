#!/usr/bin/env python3
## -*- coding: utf-8 -*-

PORT = 45678

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio
from simeb import make_link, get_bus

##############################################################################

bus = get_bus()

@bus.register
def hello(param):
  print("Hello",param)

@asyncio.coroutine
def start():
  D("start")
  make_link()
  yield from asyncio.sleep(1)
  bus.hello("world !")

def main():
  logging.basicConfig(level=logging.DEBUG)
  asyncio.Task(start())
  asyncio.get_event_loop().run_forever()
  D("done.")

if __name__ == "__main__":
  main()
  