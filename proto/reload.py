#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" Run a command on web. """

##############################################################################
## Uses

import sys # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import subprocess # http://docs.python.org/py3k/library/subprocess.html
import logging # http://docs.python.org/py3k/library/logging.html
import select # http://docs.python.org/py3k/library/select.html
log = logging.getLogger(__name__)
from util import CUI
from bottle import route, run

##############################################################################
## 
  
class Cmd:
  def __init__(self,params):
    self.params = params
    self.proc = None
    self.poll = select.poll()
    
  def begin(self):
    log.debug("begin: {0}".format(" ".join(self.params)))
    self.proc = subprocess.Popen(self.params, 
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    self.poll.register(self.proc.stdout, select.POLLIN | select.POLLHUP)
    self.poll.register(self.proc.stderr, select.POLLIN | select.POLLHUP)

  def end(self):
    self.proc.wait()
    self.proc = None

  def pull(self):
    for event in self.poll.poll():
      fd, event  = event
      ##
      if fd == self.proc.stdout.fileno():
        line = self.proc.stdout.readline()
        if len(line) == 0:
          return None
        return line.decode("utf-8").strip()
      ##
      if fd == self.proc.stderr.fileno():
        line = self.proc.stderr.readline()
        if len(line) == 0:
          return None
        return line.decode("utf-8").strip()

##############################################################################
## 
  
HEADER="""
<pre>
"""
FOOTER="""
</pre>
"""
  
@route('/')
def iter():
  cmd.begin()
  yield HEADER
  line = cmd.pull()
  while line is not None:
    yield line + "\n"
    line = cmd.pull()
  yield FOOTER
  cmd.end()
 
def argscall(parser):
  parser.add_argument("param",
    nargs=argparse.REMAINDER,
    help="parameters")
   
ui = CUI(argscall=argscall)
cmd = Cmd(ui.args.param)
run(host='localhost', port=8080, debug=True)
  
  
  