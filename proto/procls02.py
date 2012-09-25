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
import webbrowser # http://docs.python.org/py3k/library/webbrowser.html
import inspect
from bottle import route, run, jinja2_template
log = logging.getLogger(__name__)

##############################################################################
## Code

def f(s):
  caller = inspect.currentframe().f_back
  return s.format(**caller.f_locals)

def on_error(ex):
  log.error(str(ex))

def rls1():
  proc = "/proc"
  for root, dirs, files in os.walk(proc,onerror=on_error):
    log.debug("{0} {1} {2}".format(root,dirs,files))
   
@route('/')
def hello():
  jinja2_template()
  return "Hello World!"

##############################################################################
## Running
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  host='localhost'
  port=8080
  webbrowser.open(f("http://{host}:{port}"), 0, True)
  run(host=host,port=port)
  