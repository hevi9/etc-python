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
import os
j = os.path.join

##############################################################################

def find_up(name):
  path = os.getcwd().split(os.sep)
  while len(path):
    # os.sep to give root dir
    file = os.path.normpath(j(os.sep,os.sep.join(path),name))
    if os.path.exists(file):
      D("find up %s, found",file)
      return file
    else:
      D("find up %s, not exists",file)
    path.pop()
  return None

def app_name(name=None):
  if name:
    return name
  return os.path.basename(os.path.splitext(sys.argv[0])[0])
  
def control_file(appname):
  return appname + "-" + "ctrl.yaml"

  
def load_up(control):
  """ """
  
def load_home(control):
  """ """

class Control():
  pass

##############################################################################

def proto1(params):
  """ """  
  find_up(control_file(app_name()))

def proto(params):
  """ """  
  c = Control()  

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