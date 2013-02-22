#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
/proc prototyping.
"""

##############################################################################
## Uses

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
from threading import Timer 
from bottle import route, run, jinja2_template
log = logging.getLogger(__name__)

##############################################################################
## Code

pages = dict()

pages["base.html"] = """
<html>
<head>
  <title>{{ page_title }}</title>
</head>
<body>

<table width="99%" border="0">
<tr>
  <td><p>{{ page_title }}</p></td>
  <td align="right">{{ page_gen }}</td>
</tr>
<tr><td>
 <a href="/">Index</a>
 <a href="/error">Error</a>
  <a href="/procs">Procs</a> 
</td></tr>
</table>

{% block content %}
<p>NO CONTENT</p>
{% endblock %}

</body>
</html>
"""
pages["root.html"] = """
{% extends "base.html" %}
{% block content %}
<h1>FILES ({{ model.list | length}})</h1>
<table>
{% for item in model.list %}
<tr><td>{{ item }}</td></tr>
{% endfor %}
</table>
{% endblock %}
"""

pages["error.html"] = """
{% extends "base.html" %}
{% block content %}
<h1>ERRORS ({{ model.list_error | length}})</h1>
<table>
{% for item in model.list_error %}
<tr><td>{{ item }}</td></tr>
{% endfor %}
</table>
{% endblock %}
"""

pages["procs.html"] = """
{% extends "base.html" %}
{% block content %}
<h1>PROCS ({{ model.list_error | length}})</h1>
<table>
{% for item in model.procs %}
<tr><td>{{ item }}</td></tr>
{% endfor %}
</table>
{% endblock %}
"""


base_ctx = dict()
base_ctx["page_title"] = "No name"
base_ctx["page_gen"] = datetime.datetime.now().isoformat(" ")

jenv = jinja2.Environment(loader=jinja2.DictLoader(pages))

def f(s):
  caller = inspect.currentframe().f_back
  combi = dict(caller.f_globals)
  combi.update(caller.f_locals)
  return s.format(**combi)

class Model: pass

def make_model2():
  model = Model()
  model.list = list()
  model.list_error = list()
  model.proc = "/proc"
  def on_error(ex):
    model.list_error.append(str(ex))
  for root, dirs, files in os.walk(model.proc,onerror=on_error):
    for file in files:      
      model.list.append(root + "/" + file)      
  log.debug("model.list {0}".format(len(model.list)))
  model.list.sort()
  return model

def ext_proc(name,model):
  r"[0-9]+"
  if not hasattr(model, "procs"): model.procs = list()
  line = name + ":: " + " ".join(os.listdir("/proc/" + name))
  model.procs.append(line)
  return True

def make_model():
  exts = (ext_proc,)
  model = Model()
  model.list = list()
  model.list_error = list()
  model.proc = "/proc"
  def on_error(ex):
    model.list_error.append(str(ex))
  for name in os.listdir(model.proc):
    managed = False
    for ext in exts:
      if re.match(ext.__doc__,name):
        managed = True
        if ext(name,model):
          break
    if not managed:
      model.list.append(name)
  log.debug("model.list {0}".format(len(model.list)))
  model.list.sort()
  return model
        
@route('/')
def index():
  ctx = dict(base_ctx)
  ctx["page_title"] = "INDEX"
  ctx["model"] = make_model()
  return jenv.get_template("root.html").render(ctx)

@route('/error')
def error():  
  ctx = dict(base_ctx)
  ctx["page_title"] = "Error"
  ctx["model"] = make_model()
  return jenv.get_template("error.html").render(ctx)

@route('/procs')
def procs():  
  ctx = dict(base_ctx)
  ctx["page_title"] = "Procs"
  ctx["model"] = make_model()
  return jenv.get_template("procs.html").render(ctx)


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
  