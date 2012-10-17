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
from util import f
from file import File

# works ? loads a page on demand ?
pages = dict()
jenv = jinja2.Environment(loader=jinja2.DictLoader(pages))

##############################################################################
## Base

pages["base.html"] = """
<html>
<head>
<title>{{ page.title }}</title>
<style>
#nav ul {
  margin-left: 5;
  padding-left: 0;
  display: inline;
}
#nav li {
  border: 0px solid #000;
  display: inline;
}
</style>
</head>

<body>

{% block fileid %}
<table width="99%" border="0">
<tr>
  <td><p>{{ page.title }}</p></td>
  <td align="right">{{ page.gen }}</td>
</tr>
<table>
{% endblock %}

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
    """  """
    self.ctx = dict()
    self.ctx["page"] = self
    self.title = f("Base {rp}")
    self.gen = datetime.datetime.now().isoformat(" ")
    self.ctx["model"] = self.model = Model()

  def render(self):
    return type(self).tmpl.render(self.ctx)

##############################################################################
## 1 EFile

pages["file.html"] = """
{% extends "base.html" %}
{% block content %}
FILE
{% endblock %}
"""

class EFile(Base):
  tmpl = jenv.get_template("file.html")
  
  def __init__(self,file):
    super().__init__(file.path)
    self.file = file
    self.model.file = file 

##############################################################################
## 1 reg

pages["reg.html"] = """
{% extends "base.html" %}
{% block content %}
REG
{% endblock %}
"""

class Reg(EFile):
  tmpl = jenv.get_template("reg.html")
  
  def __init__(self,file):
    super().__init__(file)

##############################################################################
## 2 Dir

pages["dir.html"] = """
{% extends "base.html" %}
{% block content %}

Dirs ({{model.file_dirs | count}}): 
<div id="nav">
<ul>
{% for file in model.file_dirs | sort(attribute="name") %}
 <li><a href="{{file.path}}">{{file.name}}</a></li>
{% endfor %}
<ul>
</div>

Files 
{{model.file_files | count}}, 
{{model.file_files | sum(attribute="size") | filesizeformat}}
<table>
{% for file in model.file_files | sort(attribute="name") %}
<tr>
 <td><a href="{{file.path}}">{{file.name}}</a></td>
 <td>{{file.size | filesizeformat(binary=True)}}</tr>
</tr>
{% endfor %}
</table>

{% endblock %}
"""

class Dir(EFile):
  tmpl = jenv.get_template("dir.html")

  def __init__(self,file):
    super().__init__(file)
    self.title = f("Dir {file.path}")
    ##
    self.model.file_dirs = list()
    self.model.file_files = list()
    self.model.files = list()
    for name in file.listdir():
      sfile = file.subfile(name)
      self.model.files.append(sfile)      
      if sfile.isdir:
        self.model.file_dirs.append(sfile)
      else: 
        self.model.file_files.append(sfile)
    #log.debug(self.model.files) 

##############################################################################
## 3 Error

pages["error.html"] = """
{% extends "base.html" %}
{% block content %}
<p>
{{ model.extext }}
</p>
{% endblock %}
"""

class Error(Base):
  tmpl = jenv.get_template("error.html")

  def __init__(self,rp,ex):
    super().__init__(rp)
    self.title = f("Error {rp}")
    self.model.ex = ex
    self.model.extext = str(ex)

##############################################################################
## 4 Link

pages["link.html"] = """
{% extends "base.html" %}
{% block content %}
LINK
{% endblock %}
"""

class Link(EFile):
  tmpl = jenv.get_template("link.html")

  def __init__(self,rp):
    super().__init__(rp)

##############################################################################
## 5 Dev

pages["dev.html"] = """
{% extends "base.html" %}
{% block content %}
DEV
{% endblock %}
"""

class Dev(EFile):
  tmpl = jenv.get_template("dev.html")

  def __init__(self,rp):
    super().__init__(rp)

##############################################################################
## Code

def make_entry2(rp):  
  try:
    file = File(rp)
  except OSError as ex:
    return Error(rp,ex)
  if file.isdir:
    return Dir(file)
  elif file.ischr:
    return Base(file)
  elif file.isblk:
    return Base(file)
  elif file.isreg:
    return Reg(file)
  elif file.islnk:
    return Link(file)
  elif file.issock:
    return Base(file)
  else:
    return Error(rp,"Unknown system file")
  
def make_entry(rp):
  try:
    return make_entry2(rp)
  except Exception as ex:
    return Error(rp,ex)
  
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
  