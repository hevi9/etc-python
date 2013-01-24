#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
/proc prototyping.
"""

##############################################################################
## Uses

import os # http://docs.python.org/py3k/library/os.html
import sys # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)

##############################################################################
## Code

def on_error(ex):
  log.error(str(ex))

def rls1():
  proc = "/proc"
  for root, dirs, files in os.walk(proc,onerror=on_error):
    log.debug("{0} {1} {2}".format(root,dirs,files))
   

def run():
  rls1()

##############################################################################
## Running
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run()
  