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

'page_pslist':
"""
{% extends "page_base" %}
{% block content %}
<pre>
{{ pslist }}
</pre>
{% endblock %}
"""

} # end tmpls dict

##############################################################################
## Running

def render(environ,start_response):
  fields = parse_formvars(environ)
  start_response('200 OK', [('content-type', 'text/html')])
  ##
  env = jinja2.Environment(loader=jinja2.DictLoader(tmpls))
  ctx = dict()
  ctx["title"] = "Processes"
  #ps = sp.Popen(["ps","aux"],stdout=sp.PIPE)
  ps = sp.Popen(["ps","-A","-F","-w","--sort=-rss"],stdout=sp.PIPE)
  ctx["pslist"] = cgi.escape(ps.communicate()[0])  
  ##
  apage = env.get_template("page_pslist")
  return apage.render(ctx)
  
def run():
  ##
  host = "localhost"
  port = 22345
  app = render
  ##
  url = "http://%(host)s:%(port)d/" % vars()
  log.info("open: %(url)s" % vars())
  browser = wb.get('firefox')
  browser.open(url)
  #time.sleep(4)
  ##
  log.info("running server forever ..")
  pserver.serve(app,host=host,port=port,threadpool_workers=5)
  
  
if __name__ == "__main__":
  main = hum.Main(run=run,debug=True)
  main.start()
  