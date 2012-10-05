#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
File browser.
"""

##############################################################################
## Uses & module setup

import os # http://docs.python.org/py3k/library/os.html
import sys # http://docs.python.org/py3k/library/sys.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging # http://docs.python.org/py3k/library/logging.html
import webbrowser # http://docs.python.org/py3k/library/webbrowser.html
import inspect
import jinja2
import datetime
import time
import re
import stat # http://docs.python.org/py3k/library/stat.html
from threading import Timer 
from bottle import route, run, jinja2_template
log = logging.getLogger(__name__)

pages = dict()

# works ? loads a page on demand ?
jenv = jinja2.Environment(loader=jinja2.DictLoader(pages))

##############################################################################
## Utils

def f(s):
  """ Format text from locals and globals names. """
  caller = inspect.currentframe().f_back
  combi = dict(caller.f_globals)
  combi.update(caller.f_locals)
  return s.format(**combi)


##############################################################################
## Base

pages["base.html"] = """
<html>
<head>
  <title>{{ page.title }}</title>
</head>
<body>

<table width="99%" border="0">
<tr>
  <td><p>{{ page.title }}</p></td>
  <td align="right">{{ page.gen }}</td>
</tr>
<table>

{% block content %}
<p>NO CONTENT</p>
{% endblock %}

</body>
</html>
"""

class Model: pass

class Base:
  tmpl = jenv.get_template("base.html")

  def __init__(self,rp):
    """
    rp is request path. 
    """
    self.ctx = dict() # ???
    self.ctx["page"] = self
    self.title = f("Base {rp}")
    self.rp = rp
    self.gen = datetime.datetime.now().isoformat(" ")
    self.ctx["model"] = self.model = Model()
    self.model.path = os.path.normpath(rp) 

  def render(self):
    return Base.tmpl.render(self.ctx)

##############################################################################
## 1 File

pages["file.html"] = """
{% extends "base.html" %}
{% block content %}
FILE
{% endblock %}
"""

class File(Base):
  tmpl = jenv.get_template("file.html")
  
  def __init__(self,rp):
    super().__init__(rp)

  def render(self):
    return File.tmpl.render(self.ctx)


##############################################################################
## 2 Dir

pages["dir.html"] = """
{% extends "base.html" %}
{% block content %}
<table>
{% for file in model.files %}
<tr>
 <td><a href="{{file.path}}">{{file.name}}</a></td>
</tr>
{% endfor %}
</table>
{% endblock %}
"""

class Dir(Base):
  tmpl = jenv.get_template("dir.html")

  def __init__(self,rp,st):
    super().__init__(rp)
    self.st = st
    self.title = f("Dir {rp}")
    ##
    self.model.file_dirs = list()
    self.model.file_files = list()
    for name in os.listdir(rp):
      abspath = os.path.join(rp,name)
      file = AFile(abspath, os.lstat(abspath))
      self.model.files.append(file)
    log.debug(self.model.files) 

  def render(self):
    return Dir.tmpl.render(self.ctx)


##############################################################################
## 3 Error

pages["error.html"] = """
{% extends "base.html" %}
{% block content %}
{{ model.extext }}
{% endblock %}
"""

class Error(Base):
  tmpl = jenv.get_template("error.html")

  def __init__(self,rp,ex):
    super().__init__(rp)
    self.model.ex = ex
    self.model.extext = str(ex)

  def render(self):
    return Error.tmpl.render(self.ctx)


##############################################################################
## 4 Link

pages["link.html"] = """
{% extends "base.html" %}
{% block content %}
LINK
{% endblock %}
"""

class Link(Base):
  tmpl = jenv.get_template("link.html")

  def __init__(self,rp):
    super().__init__(rp)

  def render(self):
    return Link.tmpl.render(self.ctx)


##############################################################################
## 5 Dev

pages["dev.html"] = """
{% extends "base.html" %}
{% block content %}
DEV
{% endblock %}
"""

class Dev(Base):
  tmpl = jenv.get_template("dev.html")

  def __init__(self,rp):
    super().__init__(rp)

  def render(self):
    return Dev.tmpl.render(self.ctx)

##############################################################################
## Code

def make_entry(rp):  
  try:
    st = os.lstat(rp)
  except OSError as ex:
    return Error(rp,ex)
  mode = st.st_mode
  if S_ISDIR(mode):
    return Dir(rp,st)
  elif S_ISCHR(mode):
    return Base(rp) # XXC Char
  elif S_ISBLK(mode):
    return Base(rp) # XXC Block
  elif S_ISREG(mode):
    return File(rp)
  elif S_ISFIFO(mode):
    return Base(rp) # XXX Fifo
  elif S_ISLNK(mode):
    return Link(rp)
  elif S_ISSOCK(mode):
    return Base(rp) # XXX SOCK
  else:
    return Error(rp) # XXX Undef spesifix  
  
@route('<rp:path>')
def index(rp):
  log.debug(f("request path {rp}"))
  entry = make_entry(rp)
  return entry.render()

##############################################################################
## Running

host='localhost'
port=8080
  
def start_browser():
  webbrowser.open(f("http://{host}:{port}"), 0, True)
    
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)  
  Timer(4,start_browser).start()
  run(host=host,port=port)
  