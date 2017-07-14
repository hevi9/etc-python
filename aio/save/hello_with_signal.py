#!/usr/bin/env python3.4
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-eventloop.html

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio # http://docs.python.org/3.4/library/asyncio.html
import functools
import signal
import os

def stop_req(signame):
  print("received signal %s, stopping" % signame)
  loop.stop()

def print_and_repeat(loop):
  print("Hello")
  loop.call_later(1, print_and_repeat, loop)

loop = asyncio.get_event_loop()

def main():
  logging.basicConfig(level=logging.DEBUG)  
  for name in ("SIGINT", "SIGTERM"):
    loop.add_signal_handler(getattr(signal, name),
      functools.partial(stop_req, name))  
  loop.call_soon(print_and_repeat, loop)
  print("running forever. CTRL-c or send SIGINT or SIGTERM to process %s to stop"
        % os.getpid())
  loop.run_forever()
  D("done.")


if __name__ == "__main__":
  main()
  