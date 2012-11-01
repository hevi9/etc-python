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
import datetime # http://docs.python.org/py3k/library/datetime.html
import time # http://docs.python.org/py3k/library/time.html
import re
import stat # http://docs.python.org/py3k/library/stat.html
from threading import Timer 
from bottle import route, run, jinja2_template
log = logging.getLogger(__name__)
from util import f
from file import File

##############################################################################
## Templating

## incode template pages
pages = dict()

## jinja2 environment
jenv = jinja2.Environment(loader=jinja2.DictLoader(pages))

## date presentation filter
def date(value:float):
  return datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M")
jenv.filters["date"] = date

## short date presentation filter
def sdate(value:float):
  return datetime.datetime.fromtimestamp(value).strftime("%y%m")
jenv.filters["sdate"] = sdate

## octal
def noct(value:int):
  return "{0:o}".format(value)
jenv.filters["noct"] = noct

## file size presentation
def fsize(value:int):
  if value < 1000:
    return str(value) + "B"
  elif value < 1000000:
    sv = str(int(value / 1024))
    if len(sv) == 1:
      sv = "{0:.1f}".format(value / 1024.)
    return sv + "K"
  elif value < 1000000000:
    sv = str(int(value / (1024*1024)))
    if len(sv) == 1:
      sv = "{0:.1f}".format(value / (1024. * 1024))
    return sv + "M"
  else:
    sv = str(int(value / (1024*1024*1024)))
    if len(sv) == 1:
      sv = "{0:.1f}".format(value / (1024. * 1024 * 1024))
    return sv + "G"
jenv.filters["fsize"] = fsize

## pipe object type
def objtype(value:object):
  return str(type(value))
jenv.filters["objtype"] = objtype

  
##############################################################################
## Base

pages["base.html"] = """
<html>
<head>
<title>{{ page.title }}</title>

<style>
body {
  font-family: arial, sans-serif;
}
#nav ul {
  margin: 0;
  padding: 0;
  float: left;
  width: 100%;
  list-style-type: none;
}
#nav li {
  /* border: 0px solid #000; */
  /* display: inline; */
  appearance: button;
  -moz-appearance: button;
  padding: 2;
  float: left;
  margin: 2;
}
#nav a {
  text-decoration: none;
  color: black;
}
h1 {
  font-size: 13pt;
  margin: 0;
  padding: 0;
}
table {
  margin: 0;
  padding: 0;
}

</style>

</head>

<body>

{% block fileid %}
<table width="99%" border="0">
<tr>
  <td><p>{{ page.title }}</p></td>
  <td align="right">Gen {{ page.gen | date }}</td>
</tr>
<table>
{% endblock %}

{% block content %}
<p>NO CONTENT</p>
{% endblock %}

{% block program %}
<h1>Program</h1>
{{proc.euid}}eiud 
{{proc.egid}}egid
{{proc.pid}}pid
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
    self.gen = time.time()
    self.ctx["model"] = self.model = Model()
    self.ctx["proc"] = proc

  def render(self):
    return type(self).tmpl.render(self.ctx)

def make_rplist(rp):
  r = list()
  p = rp
  t = os.path.split(p)
  r.append(t[1])
  while t[1] is not '':
    p = t[0]
    t = os.path.split(p)
    r.append(t[1])
  r.reverse()
  return r

##############################################################################
## 1 EFile

pages["file.html"] = """
{% extends "base.html" %}
{% block content %}
<table>
{% for key in model.file.props %}
<tr>
  <td>{{key}}</td>
  <td>{{model.file.props[key]}}</td>
</tr>
{% endfor %}
</table>
{% endblock %}
"""

class EFile(Base):
  tmpl = jenv.get_template("file.html")
  
  def __init__(self,file):
    super().__init__(file.path)
    self.title = f("EFile {file.path}")
    self.file = file
    self.model.file = file 

##############################################################################
## 1 reg

pages["reg.html"] = """
{% extends "file.html" %}
{% block content %}
<pre>
{{model.data | e}}
</pre>
{% endblock %}
"""

class Reg(EFile):
  tmpl = jenv.get_template("reg.html")
  
  def __init__(self,file):
    super().__init__(file)
    self.title = f("Reg {file.path}")    
    self.model.data = self.make_file_data()
    
  def make_file_data(self):
    try:
      fd = open(self.file.path)
      data = fd.read() # utf-8 decoding
      fd.close()
    except UnicodeDecodeError as ex:
      data = make_binary_data(self.file.path)
    return data
  
## http://code.activestate.com/recipes/576945/

fhex = lambda data: ' '.join('{:02X}'.format(i) for i in data)

fstr = lambda data: ''.join(31 < i < 127 and chr(i) or '.' for i in data)
  
def make_binary_data(path):
  rdata = list()
  rdata.append("{0} first bytes from {1}:".format(16*64,path))
  file = open(path, 'rb')
  for line in range(0, min(os.path.getsize(path),16*64), 16):
    data = file.read(16)
    rdata.append('{:08X} | {:47} | {}'.format(line, fhex(data), fstr(data)))
  file.close()
  return "\n".join(rdata)
    

##############################################################################
## 2 Dir

pages["dir.html"] = """
{% extends "base.html" %}
{% block content %}

<h1>Dirs {{model.file_dirs | count}}n</h1> 
<div id="nav">
<ul>
{% for file in model.file_dirs | sort(attribute="name") %}
 <li><a href="{{file.path}}">{{file.name}}</a></li>
{% endfor %}
<ul>
</div>

<h1>Files 
{{model.file_files | count}}n 
{{model.file_files | sum(attribute="size") | fsize}}
</h1>
<table>
<thead>
 <tr>
   <th align="left">T</th>
   <th align="left">Mode</th>
   <th align="left">Name</th>
   <th align="left">Size</th>
   <th align="left">MTime</th>
 </tr>
</thead>
{% for file in model.file_files | sort(attribute="name") %}
<tr>
 <td>{{file.chtype}}</td>
 <td>{{file.mode | noct}}</td>
 <td><a href="{{file.path}}">{{file.name}}</a></td>
 <td align="right">{{file.size | fsize}}</td>
 <td>{{file.mtime | sdate }}</td>
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
{{ model.ex | objtype | e}}
</p>
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

def make_entry(rp):  
  try:
    file = File(rp)
  except OSError as ex:
    return Error(rp,ex)
  if file.isdir:
    return Dir(file)
  elif file.ischr:
    return EFile(file)
  elif file.isblk:
    return EFile(file)
  elif file.isreg:
    return Reg(file)
  elif file.islnk:
    return Link(file)
  elif file.issock:
    return EFile(file)
  else:
    return Error(rp,"Unknown system file")
  
def make_entry2(rp):
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
  
class Proc: pass
proc = Proc()
proc.host = host
proc.port = port
proc.cwd = os.getcwd()
proc.euid = os.geteuid()
proc.egid = os.getegid()
proc.pid = os.getpid()
  
def start_browser():
  webbrowser.open(f("http://{host}:{port}"), 0, True)
    
if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)  
  Timer(2,start_browser).start()
  run(host=host,port=port,debug=True)
  