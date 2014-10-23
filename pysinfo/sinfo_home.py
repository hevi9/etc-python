#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from .data import sinfo_apply 
import os 
import asyncio
import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error

import time

path = os.environ["HOME"]

def get_stats():
  nfiles = 0
  for dir, dirs, files in os.walk(path):
    nfiles += len(files)
  return nfiles  

nfiles = 0

data = {
  "path": path,
  "nfiles": nfiles
}

@asyncio.coroutine
def update_coro():
  D("update_coro() enter")  
  global nfiles
  for dir, dirs, files in os.walk(path):
    nfiles += len(files)
    data["nfiles"] = nfiles
    yield from asyncio.sleep(0.00000001)
  D("update_coro() leave")

sinfo_apply("home", data, update_coro)