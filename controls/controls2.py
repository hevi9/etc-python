#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1
""" """

import sys      # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error

##############################################################################



##############################################################################

ctrl = control()

@control_def
def debug(value):
  return value

def proto(params):
  """ """
  if crtl.debug:
    print("debug is on")

##############################################################################

ARGS = argparse.ArgumentParser()
ARGS.add_argument("params", nargs="*",
                  help="positional arguments")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")

##############################################################################

def main():
  args = ARGS.parse_args()
  logging.basicConfig(level=logging.INFO)
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  proto(args.params)
  D("done.")
  sys.exit(0)

if __name__ == "__main__":
  main()