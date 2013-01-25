#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
"""
pyild - build management system
"""

##############################################################################
## Uses & module setup

import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
from hevi_proto import *

##############################################################################
## entry

def main():
  logging.basicConfig(level=logging.DEBUG)
  log.debug("main()")
  
