#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" 
Run a command on web
==================== 

WebMake

Ability to run a make or other "build" commands from browser and
get build results into page.

Motivation

Presentation and management of build output text.

Use

Start local process webappserver in current build directory::

  /wrk/project> webmake.py
  
which open browser and runs make and redirects make stdout and stderr
into web page text.

Related

CI (Continuous Integration) frameworks.

Challenges

ansi terminal code formatting of the output text.

recursive submakes ?

Continuous output and web-frameworks and html page structure. Producing
the make output content may take 30mins but page structure needs end
html tags immediately.   

"""

##############################################################################
## Uses

import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import subprocess # http://docs.python.org/py3k/library/subprocess.html
import logging # http://docs.python.org/py3k/library/logging.html
import select # http://docs.python.org/py3k/library/select.html
import socket # http://docs.python.org/py3k/library/select.html
log = logging.getLogger(__name__)
import hevi_proto
from hevi_proto.util import CUI
from bottle import route, run
from jinja2 import Template # http://jinja.pocoo.org/docs/

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
    log.debug("end:")
    self.poll.unregister(self.proc.stdout)
    self.poll.unregister(self.proc.stderr)
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
  
tmpl_header=Template("""
<head>
<title>{{title}}</title>
<style>{{style}}</style>
</head>
<body>

<div class="topbar">
<ul>
<li>{{title}}</li>
<li>@{{hostname}}</li>
</ul>
</div>

<pre>
""")

tmpl_footer=Template("""
</body>
</pre>
""")
  
def load_style():
  stylefile = os.path.join(os.path.dirname(hevi_proto.__file__),"reload_style.css")
  log.debug("load_style: {0}".format(stylefile))
  f = open(stylefile)
  text = f.read()
  f.close()
  return text

  
@route('/')
def iter():
  data=dict()
  data["title"] = " ".join(cmd.params)
  data["style"] = tmpl_style
  data["hostname"] = socket.getfqdn()
  ##
  cmd.begin()
  yield tmpl_header.render(data)
  line = cmd.pull()
  while line is not None:
    yield line + "\n"
    line = cmd.pull()
  yield tmpl_footer.render(data)
  cmd.end()
 
def argscall(parser):
  parser.add_argument("param",
    nargs=argparse.REMAINDER,
    help="parameters")
   
if __name__ == "__main__":
  ui = CUI(argscall=argscall)
  tmpl_style = load_style()
  cmd = Cmd(ui.args.param)
  run(host='localhost', port=8080, debug=True)
  
  
  