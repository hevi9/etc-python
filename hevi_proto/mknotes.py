#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
"""
Compose home text notes into single html file
=============================================

Usage::

 > mknotes
 
Gathers all *.rst files under $home directory and
composes $home/public_html/notes.html file.
"""

import logging
log = logging.getLogger(__name__)
import argparse
import os
import fnmatch
j = os.path.join
from docutils.core import publish_parts

home = os.environ["HOME"]
counter = 0

def step(txt):
  global counter
  counter += 1
  print(counter,txt)
  
def result(txt):
  print("=>",txt)

def gather():
  results = list()
  step("Looking *.rst files under {}".format(home))
  for path, dirs, files in os.walk(home):
    for file in files:
      if fnmatch.fnmatchcase(file, "*.rst"):
        apath = j(path,file)
        log.debug(apath)
        results.append(apath)
  result("{} files found".format(len(results)))
  return results

class context:
  css = None

class Note:
  date = None
  title = None
  apath = None

def load_note(file):
  """ Load information from rst file to Note record. """
  step("Loading file {}".format(file))
  note = Note()
  docutils_settings = {}
  with open(file) as fd:
    text = fd.read()
  parts = publish_parts(
          source=text,
          source_path=file,
          writer_name="html4css1",
          settings_overrides=docutils_settings)
  # parts['body']
  return note


def main():
  parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
  parser.add_argument("-d","--debug",action="store_true",help="set logging level to debug")
  args = parser.parse_args()
  if args.debug:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig()
  notes = list()
  for file in gather():
    notes.append(load_note(file))
  
if __name__ == "__main__": main()