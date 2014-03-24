#!/usr/bin/env python3.4
## -*- coding: utf-8 -*-

import asyncio
from simeb import make_link, get_bus

bus = get_bus()

@bus.register
def echo_reply(text):
  print("echo_reply got", text)
  asyncio.get_event_loop().stop()

@asyncio.coroutine
def start():
  make_link()
  yield from asyncio.sleep(1)
  bus.echo_request("HELLOOO")

def main():
  asyncio.Task(start())
  asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
  main()
  