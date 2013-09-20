#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__      = "main"
__version__   = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__   = "$Release$"
__docformat__ = "epytext"
"""
"""

##############################################################################
## Uses

import logging
log = logging.getLogger(__name__)
import hevi_util.main as hum
import jinja2
import subprocess as sp
import webbrowser as wb
from paste.request import parse_formvars
import paste.httpserver as pserver
import time
import cgi
from hevi_util.common import *
import hevi_misc.tagtree as tt
import threading


##############################################################################
##

tmpls = {

"page_base":
"""
<html>
<head>
<title>{{ title }}</title>
</head>
<body>
<h1>{{ title }}</h1>
{% block content %}
NO CONTENT
{% endblock %}
</body>
</html>
""", 

'page_content':
"""
{% extends "page_base" %}
{% block content %}

<h2>Compact table</h2>
<pre>
{{ compact_table }}
</pre>

{% endblock %}
""",

'page_all_entries':
"""
{% extends "page_base" %}
{% block content %}

<h2>All Entries</h2>
<ol>
{% for entry in entries %}
<li><a href="file:{{ entry.path_abs() }}">{{ entry.path_rel() }}</a></li>
{% endfor%}
</ol>

{% endblock %}
"""


} # end tmpls dict

##############################################################################
## App

class App(object):
  def __init__(self):
    self.on_init()
    
  def on_init(self):
    log.debug("App.on_init")
    ## setup jinja
    self.tmplenv = jinja2.Environment(loader=jinja2.DictLoader(tmpls))
    self.ctx = dict()
    self.ctx["title"] = "Tree"
    ## Tree
    self.tree = tt.Tree()
    rl = "/home/hevi/wrk"
    self.builder = tt.Builder(self.tree)
    self.builder.build_in_dir(rl)
    log.debug("App.on_init: Tree: %d files" % len(self.tree.files()))
    log.debug("App.on_init: Tree: %d entries" % len(self.tree.entries()))
    ##
    self.ctx["entries"] = self.tree.entries()
    self.ctx["compact_table"] = self.make_compact_table()
  
  def on_shutdown(self):
    log.debug("App.on_shutdown")

  def __call__(self,environ,start_response):
    fields = parse_formvars(environ)
    start_response('200 OK', [('content-type', 'text/html')])
    ## Render
    apage = self.tmplenv.get_template("page_all_entries")
    return apage.render(self.ctx)

  def make_compact_table(self):
    pass
  

##############################################################################
## Running

def open_url(url):
  log.info("open: %(url)s" % vars())
  browser = wb.get('firefox')
  browser.open(url)
  
def run():
  ##
  host = "localhost"
  port = 22345
  app = App()
  url = "http://%(host)s:%(port)d/" % vars()
  ##
  threading.Timer(2,open_url,(url,)).start()
  ##
  server = pserver.serve(app,host=host,port=port,start_loop=False,threadpool_workers=5)
  log.info("running server forever ..")
  server.serve_forever()
  
if __name__ == "__main__":
  main = hum.Main(run=run,debug=True)
  main.start()
  