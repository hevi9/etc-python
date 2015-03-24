#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" """

##############################################################################
## Uses
import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import logging # http://docs.python.org/py3k/library/logging.html
import datetime
import jinja2
log = logging.getLogger(__name__)
from hevi_home.home_web import *

#############################################################################
## 

pages = dict(Web.base_pages)

pages["page_stats.html"] = """
{% extends "base.html" %}
{% block content %}
<h1>Home Stats</h1>
<table>
<tr><td>Entries</td> <td>{{ s_entry_count  }}</td></tr>
<tr><td>Files</td> <td>{{ s_file_count  }}</td></tr>
<tr><td>Files total size</td> <td>{{ s_file_size  }}</td></tr>
<tr><td>Dirs</td> <td>{{ s_dir_count  }}</td></tr>
<tr><td>Others</td> <td>{{ s_other_count  }}</td></tr>
</table>

<h1>Powerview</h1>
<pre>{{ powerview }}</pre>
{% endblock %}
"""

pages["index.html"] = """
{% extends "base.html" %}
{% block content %}

<h1>Pages</h1>
<ol>
{% for entry in tree.tags()["html"].entries().values() %}
  <li>{{ entry.path() }}</li>
{% endfor %}
</ol>

<h1>Tags [{{ tags | length }}]</h1>
<ol>
{% for tag in tags %}
  <li> {{ tag.name() }} {{ tag.entries() | length }} </li>
{% endfor %}
</ol>
{% endblock %}
"""

pages["files.html"] = """
{% extends "base.html" %}
{% block content %}

<h1>Files</h1>
<table>

{% for entry in tree.index().values() %}
<tr>
  <td>{{ entry.name() }}</td>
  <td>{{ entry.path() }}</td>
</tr>
{% endfor %}

</table>

{% endblock %}
"""


#############################################################################
## 

jenv = jinja2.Environment(loader=jinja2.DictLoader(pages))

#############################################################################
##   

def begin_report_stats(home):
  home.web.navi.append(home.web.url("home_stats.html"))
    
def cmd_report_stats(home):
  """ Report home statictics into html page. """
  ## calculate stats
  ctx = dict(home.web.base_ctx())
  ctx["page_title"] = "Home statistics"
  ctx["s_entry_count"] = 0
  ctx["s_file_count"] = 0
  ctx["s_file_size"] = 0
  ctx["s_dir_count"] = 0
  ctx["s_other_count"] = 0
  ctx["powerview"] = None
  text = "\n"
  text_count = 1
  for entry in home.tree.index().values():
    ctx["s_entry_count"] += 1
    ##
    if entry.type() == "file":
      ctx["s_file_count"] += 1
      ctx["s_file_size"] += entry.size()
    elif entry.type() == "dir":
      ctx["s_dir_count"] += 1
    else:
      ctx["s_other_count"] += 1
    # power view
    text += entry.type_char()
    if text_count % 120 == 0:
      text += "\n"
    text_count += 1
  ctx["powerview"] = text
  ## make page
  tmpl = jenv.get_template("page_stats.html")
  out = os.path.join(home.root,"public_html","home_stats.html")
  log.debug("generating {0}".format(out))
  fdw = open(out,"w")
  fdw.write(tmpl.render(ctx))
  fdw.close()

def begin_tag_by_ext(home):
  """ """
  entries = list(home.tree.index().values())
  for entry in entries:
    base, ext = os.path.splitext(entry.name())
    if ext == ".html":
      entry.tag_insert("html")
      entry.type_char("h")
    elif ext == ".py":
      entry.tag_insert("python")
      entry.type_char("p")
    elif ext == ".c":
      entry.tag_insert("c")
      entry.type_char("c")
    elif ext == ".txt":
      entry.tag_insert("text")
      entry.type_char("t")
    else:
      if ext is not "":
        entry.tag_insert(ext)
        entry.tag_insert("auto")

def begin_tag_by_location(home):
  """ """
  entries = list(home.tree.index().values())
  for entry in entries:
    nl = [e.name() for e in entry.epath()]
    if "public_html" in nl:
      entry.tag_insert("public")
    elif "Trash" in nl:
      entry.tag_insert("trash")
    elif "cache" in nl:
      entry.tag_insert("cache")
    elif "Cache" in nl:
      entry.tag_insert("cache")
    elif "__pycache__" in nl:
      entry.tag_insert("cache")


def cmd_report_index(home):
  """ Make public_html index page. """
  ## Make context
  ctx = dict(home.web.base_ctx())
  ctx["page_title"] = "Index"
  ctx["tags"] = home.tree.tags().values()
  ## make page
  tmpl = jenv.get_template("index.html")
  out = os.path.join(home.root,"public_html","index.html")
  log.info("generating {0}".format(out))
  fdw = open(out,"w")
  fdw.write(tmpl.render(ctx))
  fdw.close()

def xcmd_report_files(home):
  """ Make public_html index page. """
  ## Make context
  ctx = dict(home.web.base_ctx())
  ctx["page_title"] = "Files"
  ctx["tags"] = home.tree.tags().values()
  ## make page
  tmpl = jenv.get_template("files.html")
  out = os.path.join(home.root,"public_html","files.html")
  log.debug("generating {0}".format(out))
  fdw = open(out,"w")
  fdw.write(tmpl.render(ctx))
  fdw.close()




