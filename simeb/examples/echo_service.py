#!/usr/bin/env python3.4
## -*- coding: utf-8 -*-

import asyncio
from simeb import get_bus

bus = get_bus()

@bus.register
def echo_request(text):
  print("echo_request got", text)
  bus.echo_reply(text + " TOO")

if __name__ == "__main__":
  print("looping forever ..")
  asyncio.get_event_loop().run_forever()
  