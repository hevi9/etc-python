#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
Web process list
================

Presenting linux process list in web efficient way. 

Resources

  * http://pypi.python.org/pypi/psutil
  * http://code.google.com/p/psutil/

"""

##############################################################################
## Uses & module setup

import os # http://docs.python.org/py3k/library/os.html
import sys # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging # http://docs.python.org/py3k/library/logging.html
import webbrowser # http://docs.python.org/py3k/library/webbrowser.html
import inspect
import jinja2
import datetime # http://docs.python.org/py3k/library/datetime.html
import time # http://docs.python.org/py3k/library/time.html
import re
import stat # http://docs.python.org/py3k/library/stat.html
from threading import Timer 
from bottle import route, run, jinja2_template
log = logging.getLogger(__name__)
from hevi_proto.util import f
from hevi_proto.file import File

##############################################################################
## Routes

@route('/')
def root():
  return "ROOT"

##############################################################################
## Running

host='localhost'
port=8080
  
def start_browser():
  webbrowser.open(f("http://{host}:{port}"), 0, True)
    
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)  
  Timer(2,start_browser).start()
  run(host=host,port=port,debug=True)

