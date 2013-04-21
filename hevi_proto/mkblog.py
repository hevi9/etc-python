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
from hevi_util.files import mkdir 
import jinja2
from hevi_proto.reader_rest import read
from pygments.formatters import HtmlFormatter

##############################################################################
## Module control

home = os.environ["HOME"]

control = {
  "name": os.path.basename(os.getcwd()),
  "root": os.getcwd(),
  "include": [ "*.rst" ],
  "ignore": [ "README.rst" ]
}
control["outdir"] = j(home,"public_html",control["name"])

##############################################################################
## Page templates

## incode template pages
pages = dict()

## jinja2 environment
jinja = jinja2.Environment(loader=jinja2.DictLoader(pages))

## base page layout
pages["base.html"] = """
<html>
<head>
<title>{{ page.title }}</title>

<style>
body {
  font-family: arial, sans-serif;
  background: #000;
}
div.documentwrapper {
    width: 80%;
    /* margin: auto; */
    /* margin-right: auto; */
    float: left;
    margin: 0px;
}

div.index {
  /* position: absolute:
  top: 0px; */
  width: 20%;
  float: right;
  margin: 0px;
}

div.article {
  background: #FFF;
  padding: 5px;
  padding-top: 3px;
  margin: 10px;
  border-style:solid;
  border-color: #888;
  border-width: 3px;
  border-radius: 10px;
  min-width: 300pt;
}

div.pointer {
  background: #FFF;
  padding: 5px;
  padding-top: 3px;
  margin: 10px;
  margin-left: 0px;
  border-style:solid;
  border-color: #888;
  border-width: 3px;
  border-radius: 10px;
}


h1 {
  margin-top: 0px;
  margin-bottom: 2pt;
  padding: 0px;
}
h1 a {
  text-decoration:none;
  color: #000;
}

div.date {
  color: green;
  /* display: inline; */
  /* position: fixed;
  left: 0pt;
  top: 0pt;
  */
}

.tags {
  float: right;
  clear: both;
}

{{ page.csspygments }}
</style>

</head>
<body>

<div class="documentwrapper">
{% block content %}
<p>NO CONTENT</p>
{% endblock %}
</div> 

<div class="index">
<div class="pointer">
<p>INDEX</p>
</div>
</div>

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
<div class="date">{{ article.date }}</div>
<div class="tags">
{% for tag in article.tags %}
<a href="{{tag}}.html">{{tag}}</a>
{% endfor %}
</div>
{{ article.body }}
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

def make_article(file):
  step("Loading {}".format(file))
  article = Article()
  article.file = file
  article.rurl = os.path.splitext(os.path.basename(file))[0] + ".html"
  article.body, info = read(file)
  article.title = info["title"]
  article.date = info["date"]
  article.tags = info["tags"]
  return article

##############################################################################
## Generate

def generate(articles):
  ofile = j(control["outdir"],"index.html")
  step("Generating {}".format(ofile))
  tmpl = jinja.get_template("index.html")
  page = {
    "title": control["name"],
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
      "csspygments": HtmlFormatter().get_style_defs('.highlight')
    }
    mkdir(os.path.dirname(ofile))
    with open(ofile,"w") as fd:
      fd.write(tmpl.render({"page": page, "article": article}))

    

##############################################################################
## Running the program

def main():
  logging.basicConfig(level=logging.DEBUG)
  step("Composing blog '{name}' to {outdir}".format(**control))
  articles = list()
  for file in collect():
    articles.append(make_article(file))
  articles.sort(key=lambda a: a.date,reverse=True)
  generate(articles)
  step_result("done")

if __name__ == "__main__": main()