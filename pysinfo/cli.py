#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

import sys      # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__package__)
D = log.debug
I = log.info
E = log.error
from pysinfo import sinfo
from pprint import pprint

##############################################################################



##############################################################################

ARGS = argparse.ArgumentParser()
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")

def setup_logging(args):
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  else:
    logging.getLogger().setLevel(logging.INFO)

def main():
  args = ARGS.parse_args()
  setup_logging(args)
  pprint(sinfo)
  sys.exit(0)


if __name__ == "__main__":
  main()
  