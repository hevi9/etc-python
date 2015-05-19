#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
What is this.
"""

##############################################################################
## Uses

import sys # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
import apt_pkg # http://apt.alioth.debian.org/python-apt-doc/library/apt_pkg.html
import apt
import apt.progress.base

##############################################################################
## Code

class Progress(apt.progress.base.OpProgress):
  
  def done(self):
    log.debug("{0} {1} DONE".format(self.op,self.subop))
  
  def update(self):
    log.debug("{0} {1}".format(self.op,self.subop))

def run():
  apt_pkg.init()
  cache = apt_pkg.Cache(Progress())
  #
  for pf in cache.file_list:
    log.debug("{0}".format(pf.filename)) 

##############################################################################
## Running

args = None
parser = argparse.ArgumentParser(description=__doc__.strip())
  
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  args = parser.parse_args()
  run()
  