#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1

"""
Blog composer and publisher
===========================

Usage::
 > cd myblog/
 > mkblog
"""

##############################################################################
## Uses and setups

import os # http://docs.python.org/3/library/os
j = os.path.join
import fnmatch # http://docs.python.org/3/library/fnmatch
import logging # # http://docs.python.org/3/library/os
log = logging.getLogger(__name__)
from hevi_util.files import mkdir, find_tree_match
import jinja2
from hevi_proto.reader_rest import read
from pygments.formatters import HtmlFormatter
import shutil
import zlib

##############################################################################
## Module control

home = os.environ["HOME"]

control = {
  "name": os.path.basename(os.getcwd()),
  "root": os.getcwd(),
  "include": [ "*.rst" ],
  "ignore": [ "README.rst", "footer.rst" ],
  "footer": "footer.rst"
}
control["outdir"] = j(home,"public_html",control["name"])

##############################################################################
## Page templates

## incode template pages
pages = dict()

## jinja2 environment
jinja = jinja2.Environment(loader=jinja2.DictLoader(pages))

## pipe object type
def color(text: str):
  return zlib.crc32(text.encode()) % 360

jinja.filters["color"] = color

## pipe object type
def date(date):
  return date.strftime("%Y-%m")

jinja.filters["date"] = date



## base page layout
pages["base.html"] = """
<!DOCTYPE html>
<html>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<head>
<title>{{ page.title }}</title>

<style>
body {
  font-family: arial, sans-serif;
  background: #000;
}
div.documentwrapper {
  width: 80%;
  float: left;
  margin: 0pt;
}

div.index {
  width: 20%;
  float: right;
  margin: 0pt;
  margin-top: 10pt;
}

.bat {
  font-family: arial, sans-serif;
  color: #FFF;
  font-size: 500%;
  /* background: #888; */
}

div.article {
  background: #FFF;
  padding: 5pt;
  padding-top: 3pt;
  margin: 10pt;
  border-style:solid;
  border-color: #888;
  border-width: 3pt;
  border-radius: 5pt;
  min-width: 300pt;
}

.logo {
  display: block;
  width: 80%;
  background: #FFF;
  padding: 5pt;
  border-style:solid;
  border-color: #888;
  border-width: 3pt;
  border-radius: 5pt;
  text-align: center;
  color: #000;
  text-decoration: none;
  font-family: Impact, Charcoal, sans-serif;
  font-size: 200%;
  font-weight: bold;
  margin-bottom: 10pt;
}


h1 {
  margin-top: 0pt;
  margin-bottom: 2pt;
  padding: 0pt;
}
h1 a {
  text-decoration:none;
  color: #000;
}

.info {
  /* float: right; */
  margin-top: 5pt;
  text-align: right;
}

div.date {
  display: inline;
}

.tags {
  display: inline;
}

.tag {
  background: hsla(120,30%,60%,1);  
  padding-left: 5pt;
  padding-right: 5pt;
  border-style:solid;
  border-color: #888;
  border-width: 2pt;
  border-radius: 5pt;  
  text-align: center;
  color: #000;
  text-decoration: none;  
}

.tag-space-ul {
  list-style-type: none;
  padding: 0pt;
  margin: 0pt;
}

.tag-space {
  display: inline-block;
  margin-bottom: 7pt;
}

{{ page.csspygments }}


.highlight, .literal-block {
  background: #EEE;  
  padding-left: 5pt;
  padding-right: 5pt;
  border-style:solid;
  border-color: #888;
  border-width: 2pt;
  border-radius: 5pt;
}

.footer {
  foreground: #FFF;
  clear: both;
  text-align: center;
  color: #DDD;
  text-decoration: none;  
  font-size: 90%;
}

.footer a {
  color: #DDD;  
}


</style>

</head>
<body>

<div class="documentwrapper">
{% block content %}
<p>NO CONTENT</p>
{% endblock %}
</div> 

<div class="index">

<a class="logo" href="index.html">{{ page.logo }}</a>

<ul class="tag-space-ul">
{% for tag in page.tags %}
<li class="tag-space">
<a class="tag" style="background:hsla({{tag|color}},30%,60%,1);" href="{{tag}}.html">{{tag}}</a>
</li>
{% endfor %}
</ul>

</div>

{% block footer %}
{% if page.footer %}
<div class="footer">
{{page.footer}}
</div>
{% endif %}
{% endblock %}

</body>
</html>
"""

## index page
pages["index.html"] = """
{% extends "base.html" %}
{% block content %}

{% for article in articles %}
<div class="article">

<h1><a href="{{article.rurl}}">{{article.title}}</a></h1>
{{ article.body }}

<div class="info">
<div class="tags">
{% for tag in article.tags %}
<a class="tag" style="background:hsla({{tag|color}},30%,60%,1);" href="{{tag}}.html">{{tag}}</a>
{% endfor %}
</div>
</div>

</div>
{% endfor %}

{% endblock %}
"""

## index page
pages["page.html"] = """
{% extends "base.html" %}
{% block content %}
<div class="article">
<h1><a href="{{article.rurl}}">{{article.title}}</a></h1>
<div class="date">{{ article.date }}</div>
<div class="tags">
{% for tag in article.tags %}
<a href="{{tag}}.html">{{tag}}</a>
{% endfor %}
</div>
{{ article.body }}
</div>
{% endblock %}
"""


##############################################################################
## Console output

counter = 0
def step(txt):
  global counter
  counter += 1
  print("{}. {}".format(counter,txt))
  
def step_result(txt):
  print("=>",txt)

def error(txt):
  print("??",txt)

##############################################################################
## gathering files

def collect():
  """ Collect articles under root tree. """
  step("Collecting articles form {}".format(control["root"]))
  result = list()
  for top, dirs, files in os.walk(control["root"]):
    ## remove ignores from files and dirs
    for file in files:
      for match in control["ignore"]:
        if fnmatch.fnmatch(file, match):
          files.remove(file)
    for dir in dirs:
      for match in control["ignore"]:
        if fnmatch.fnmatch(dir, match):
          files.remove(dir)
    ## collect
    for file in files:
      for match in control["include"]:
        if fnmatch.fnmatch(file, match):
          result.append(os.path.join(top,file))
  step_result("{} files".format(len(result)))
  return result

##############################################################################
## Article management

class Article:
  body = None
  title = None
  date = None
  tags = None
  file = None
  rurl = None # reltive url

def make_article(file,manager):
  step("Loading {}".format(file))
  article = Article()
  article.file = file
  article.rurl = os.path.splitext(os.path.basename(file))[0] + ".html"
  article.body, info = read(file, manager)
  article.title = info["title"]
  article.date = info["date"]
  manager.add_tag(date(article.date))
  article.tags = info["tags"]
  article.tags.add(date(article.date))
  for tag in article.tags:
    manager.add_tag(tag)
  return article

##############################################################################
## Generate

def generate(articles, manager):
  ofile = j(control["outdir"],"index.html")
  step("Generating {}".format(ofile))
  tmpl = jinja.get_template("index.html")
  page = {
    "title": control["name"],
    "logo": control["name"],
    "tags": sorted(manager.tags),
    "footer": manager.footer,
    "csspygments": HtmlFormatter().get_style_defs('.highlight')
  }    
  ##
  mkdir(os.path.dirname(ofile))
  with open(ofile,"w") as fd:
    fd.write(tmpl.render({"page": page, "articles": articles}))
  ## per page
  for article in articles:
    ofile = j(control["outdir"],article.rurl)
    step("Generating {}".format(ofile))
    tmpl = jinja.get_template("page.html")
    page = {
      "title": article.title,
      "logo": control["name"],
      "tags": manager.tags,
      "footer": manager.footer,
      "csspygments": HtmlFormatter().get_style_defs('.highlight')
    }
    mkdir(os.path.dirname(ofile))
    with open(ofile,"w") as fd:
      fd.write(tmpl.render({"page": page, "article": article}))
  ## copy external files
  for dst, src in manager.ext_files.items():
    step("Copy {} => {}".format(src, j(control["outdir"],dst)))
    shutil.copy(src, j(control["outdir"],dst))
    

##############################################################################
## 

class Manager:
  """ Manage the reources. """
  
  def __init__(self):
    self._ext_files = dict() # relative url => abs path  
    self._tags = set()
    self._footer = None

  def ext_file(self, file):
    files = find_tree_match(control["root"], file)
    if len(file) > 0:
      rurl = os.path.relpath(files[0], control["root"])
      src = files[0]
      self._ext_files[rurl] = src
    else:
      error("external file {} not found".format(file))
    return rurl

  def add_tag(self, tag):
    self._tags.add(tag)

  def set_footer(self, footer_html):
    self._footer = footer_html

  @property
  def ext_files(self):
    return self._ext_files

  @property
  def tags(self):
    return self._tags

  @property
  def footer(self):
    return self._footer


##############################################################################
## Running the program

def main():
  logging.basicConfig(level=logging.DEBUG)
  step("Composing blog '{name}' to {outdir}".format(**control))
  manager = Manager()
  articles = list()
  for file in collect():
    articles.append(make_article(file, manager))
  step_result("{} external files".format(len(manager.ext_files)))
  articles.sort(key=lambda a: a.date,reverse=True)
  if control.get("footer"):
    manager.set_footer(read(control.get("footer"), manager)[0])
  generate(articles, manager)
  step_result("done")

if __name__ == "__main__": main()