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

##############################################################################

class Broker:
  
  def __init__(self):
    pass
  
  
  
  
__broker = None

def broker():
  global __broker
  if not __broker:
    __broker = Broker()
  return __broker