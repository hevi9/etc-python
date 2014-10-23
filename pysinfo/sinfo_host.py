#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from .data import sinfo_apply 
import socket
import ipaddress
import sys
import asyncio
import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error


def get_ipv4():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('google.com', 0))
  addr = s.getsockname()[0]
  s.close()
  return addr

data = {
  "name": socket.gethostname(),
  "ipv4": get_ipv4(),
  "ostype": sys.platform
}

@asyncio.coroutine
def update_coro():
  D("update_coro()")

sinfo_apply("host", data, update_coro)
