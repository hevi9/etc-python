#!/usr/bin/env python
## -*- coding: iso-8859-15 -*-
## $Id$
## MAIN

"""  """

import sys
import os
import logging
log = logging.getLogger(__name__)

import StringIO as sio

input1 = """
/a/b/c/d
/a/b/c/e
/a/b/e
/a/a/a
/a/a
/a
r/3
r/5/6
"""

class Manage(object):
  
  def __init__(self):
    self._root = dict()
    self._sep = os.path.sep
  
  def parse(self,input):
    """
    :input: input stream
    """
    for line in input:
      line = line.strip()
      if len(line) == 0:
        continue
      #print "'%(line)s'" % vars()
      path = os.path.normpath(line)
      names = path.split(self._sep)
      def _insert(cur,names):
        if len(names) == 0:
          return
        name = names.pop(0)
        if not cur.has_key(name):
          cur[name] = dict()
        _insert(cur[name],names)
      _insert(self._root,names)
    
  def report(self):
    self._indent = 0
    def _print(cur):
      if len(cur) == 0:
        return
      for name in cur:
        print "  " * self._indent,name
        self._indent += 1
        _print(cur[name])
        self._indent -= 1
    _print(self._root)
      

def run():
  #input = sio.StringIO(input1)
  input = sys.stdin
  m = Manage()
  m.parse(input)
  m.report()
  
if __name__ == '__main__':
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  run()
  