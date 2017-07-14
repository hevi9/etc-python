#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

import sys      # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error
import asyncio
import aiohttp

loop = asyncio.get_event_loop()

OUT = "/tmp/out.html"

##############################################################################


class HttpRequestHandler(aiohttp.server.ServerHttpProtocol):
  
  @asyncio.coroutine
  def handle_request(self, message, payload):

##############################################################################

PROXY = "http://localhost:9999"

def get1():
  url = "http://python.org"
  connector = aiohttp.ProxyConnector(proxy=PROXY)
  D("http get from %s ..", url)
  req = yield from aiohttp.request("get", url, connector=connector)
  with open(OUT,"bw") as fo:
    while True:
      chunk = yield from req.content.read(8016)
      if not chunk:
        break    
      fo.write(chunk)
  I("get %s => %s", url, OUT)


##############################################################################

ARGS = argparse.ArgumentParser()
ARGS.add_argument("params", nargs="*",
                  help="Positional arguments")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")


def setup_logging(args):
  logging.basicConfig(level=logging.INFO)
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  logging.getLogger("asyncio").setLevel(logging.INFO)

def main():
  args = ARGS.parse_args()
  setup_logging(args)
  asyncio.async(get1())
  loop.run_forever()
  sys.exit(0)


if __name__ == "__main__":
  main()
  