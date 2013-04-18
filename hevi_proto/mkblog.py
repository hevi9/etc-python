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
from docutils.core import publish_parts
from hevi_util.files import mkdir 
import jinja2

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

{% block content %}
<p>NO CONTENT</p>
{% endblock %}

</body>
</html>
"""

## index page
pages["index.html"] = """
{% extends "base.html" %}
{% block content %}
{% for article in articles %}
{{ article.body }}
{% endfor %}
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
  tags = list()
  file = None

def load_article(file):
  step("Loading {}".format(file))
  article = Article()
  article.file = file
  docutils_settings = {}
  with open(file) as fd:
    text = fd.read()
  parts = publish_parts(
          source=text,
          source_path=file,
          writer_name="html4css1",
          settings_overrides=docutils_settings)
  article.body = parts["body"]
  print(type(parts["docinfo"])) 
  return article

##############################################################################
## Generate

def generate(articles):
  ofile = j(control["outdir"],"index.html")
  step("Generating {}".format(ofile))
  tmpl = jinja.get_template("index.html")
  page = {"title": control["name"]}
  mkdir(os.path.dirname(ofile))
  with open(ofile,"w") as fd:
    fd.write(tmpl.render({"page": page, "articles": articles}))
  

##############################################################################
## Running the program

def main():
  logging.basicConfig(level=logging.DEBUG)
  step("Composing blog '{name}' to {outdir}".format(**control))
  articles = list()
  for file in collect():
    articles.append(load_article(file))
  generate(articles)
  step_result("done")

if __name__ == "__main__": main()