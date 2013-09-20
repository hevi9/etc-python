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
import subprocess as sp
import webbrowser as wb
import time
import cgi
import threading

import jinja2
import paste.httpserver as pserver
from paste.request import parse_formvars

import hevi_util.main as hum
from hevi_util.common import *
import hevi_misc.tagtree as tt

import proto.action01 as ac
import proto.builder01 as bl

##############################################################################
##

tmpls = {

"page_base": # page_base
"""
<html>
<head>
<title>{{ title }}</title>

<style>
* {
 margin: 0;
}
body {
 font-family: Arial, Verdana, sans-serif;
 font-size: 11pt;
 padding: 0;
 margin: 0;
 border: 0;
}
#footer {
 position: relative;
 bottom: 0;
 width: 100%;
 /* height: 100%; */
 text-align: center;
 font-size: 10pt;
 color: #111;
 background-color: #eee;
 padding: 10px;
}
#top {
 color: #111
 background-color: #eee; 
}

ul.nav {
 list-style-type: none;
 font-size: 10pt;
}
li.nav {
 float: left;
 left: 5pt;
 font-size: 10pt;
}

</style>

</head>
<body>

<table width="100%" cellspacing="0" cellpadding="0" border="0" align="center">

<tr>
<td><h1>{{ title }}</h1></td>
<td valign="top">
<h1>Tree</h1>
</td>
</tr>

<tr>
<td>
{% block content %}
NO CONTENT
{% endblock %}
</td>
<td valign="top">
NAVIGATION
<ul class="nav">
{% for name,tag in tree.tags() | dictsort %}
<li class="nav">
<a href="/__tag__/{{ tag.name() }}">{{ tag.name() }}</a>({{ tag.entries() | count }})</li>
{% endfor %}
</ul>
</td>
</tr>

</table>

<div id="footer">
FOOTER
<div>

</body>
</html>
""", # end page_base

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

'page_all_entries': # page_all_entries
"""
{% extends "page_base" %}
{% block content %}

<h2>All Entries</h2>
<ol>
{% for entry in entries %}
<li><a href="file:{{ entry.path_abs() }}">{{ entry.path_rel() }}</a>
 {% for tag in entry.tags() %}
 {{ tag.name() }}
 {% endfor %}
</li>
{% endfor%}
</ol>

{% endblock %}
""", # end page_all_entries

'page_request':
"""
{% extends "page_base" %}
{% block content %}

<h2>Request</h2>
<table>
{% for key in environ %}
<tr><td>{{ key }}</td><td> {{ environ[key] }} </td></tr>
{% endfor%}
</table>

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
    self.builder = bl.Builder(self.tree)
    self.builder.build_in_dir(rl)
    self._builder2 = bl.TagBuilder(self.tree)
    self._builder2.start()
    log.debug("App.on_init: Tree: %d files" % len(self.tree.files()))
    log.debug("App.on_init: Tree: %d entries" % len(self.tree.entries()))
    ##
    self.ctx["tree"] = self.tree
    self.ctx["entries"] = self.tree.entries()
    self.ctx["compact_table"] = self.make_compact_table()
  
  def on_shutdown(self):
    log.debug("App.on_shutdown")

  def __call__(self,environ,start_response):
    fields = parse_formvars(environ)
    start_response('200 OK', [('content-type', 'text/html')])
    ## Dispatch
    ##  *type*(entry) => action(entry) 
    ## Render
    self.ctx["title"] = "Request"
    self.ctx["fields"] = fields
    self.ctx["environ"] = environ
    
    req_path = environ["PATH_INFO"]
    log.debug("request path: " + req_path)
    
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
  