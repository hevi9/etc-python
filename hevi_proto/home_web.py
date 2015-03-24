#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" Home web files management. """

#############################################################################
## Uses and setup

import os # http://docs.python.org/py3k/library/os.html
j = os.path.join
from urllib.parse import urlparse # http://docs.python.org/py3k/library/urllib.parse.html
import datetime # http://docs.python.org/py3k/library/datetime.html
__all__ = list()

#############################################################################
## Web

_base_pages = {
"base.html":
"""
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
<tr>
<td><a href="file:///home/hevi/public_html/index.html">Index</a>
</td>
<td></td>
</tr>
</table>

{% block content %}
<p>NO CONTENT</p>
{% endblock %}

</body>
</html>
"""}

__all__.append("Web")
class Web:
  """ Web resources for common content generation hub object. 
  """
  base_pages = _base_pages
  
  def __init__(self,home,root=j(os.environ["HOME"],"public_html")):
    """ root is root directory of web content tree, usually
    ~/public_html .
    """
    ## properties
    self.home = home
    self.root = root 
    self.navi = list() # as list of str as url
    ## jinja2 base context
    c = self._base_ctx = dict()
    c["prefix"] = self.home.prefix
    c["public_html"] = self.root
    c["tree"] = self.home.tree
    c["page_title"] = "NO TITLE"
    c["page_gen"] = datetime.datetime.now().isoformat(" ")

  def base_ctx(self):
    """ Prepare and return base page data jinja2 context. 
    Returns ctx as dict of str to ( str or object ). """
    ## make navigation block
    block = list()
    block.append("<ul>\n")
    for link in self.navi:
      parts = urlparse(link)
      block.append('<li><a href="{0}">{0}</a></li>\n'.format(link,parts.path))
    block.append("</ul>\n")
    self._base_ctx["page_navi"] = "".join(block)
    return self._base_ctx

  def url(self,path):
    """ Make URL from path relative to root.
    Form of url changes depending if static or dynamic system. 
    """
    return "file://" + self.root + "/" + path
    
