#!/usr/bin/env python
## -*- coding: utf-8 -*-
## $Id$
## MAIN

"""  """

##############################################################################
## Uses

import sys
import os
import logging
log = logging.getLogger(__name__)
import wsgiref.simple_server as wsgi
import webbrowser as wb
from paste.request import parse_formvars
import paste.httpserver as pserver
import jinja
import hevi.filebrowser.session as session
import fnmatch

##############################################################################
## App

_text = """
<head>
<title>Listing</title>
</head>

<h2>URLS</h2>
<ul>
{% for url in urls %}
<li>
<a href="{{url}}">{{url|e}}</a>
</li>
{% endfor %}
</ul>

<br/><b>WSGI environ<b>
<table>
{% for key in environ_keys %}
<tr>
<td>{{key}}</td><td>{{environ[key]|e}}</td>
</tr>
{% endfor %}
</table> 
"""

_urls = [
  "/test",
  "test",
  "a/b/c",
  "path/?juu=ei&action=joo"
]

##############################################################################
## CSS

_css_text = """
#dirlist { 
 margin-left: 0;
 padding-left: 0;
 margin: 0px; 
 font: 10pt verdana, arial, sans-serif;
}

#dirlist li
{
 float: left;
 width: 10em;
 /* width: auto; */
 list-style-type: none;
 text-align: left;
}

#dirlist li a
{
 display: block;
 padding: 2px;
 background-color: #ccc;
 color: #333;
 text-decoration: none;
 margin: 1px;
 border: 1px solid #000;
}

#dirlist li a:hover
{
 background-color: #666;
 color: #fff;
}

#clear {
 clear: both;
}
""" 


##############################################################################
## 

_reg_render_tmpl = """
<h1>{{file.type_text}} {{file.name}}</h1>
"""

##############################################################################
## Dir

_dir_render_tmpl = """
<h1>{{file.type_text}} {{file.name}}</h1>
{{file.path}}

Directories<br/>
<ul id="dirlist">
{% for subfile2 in list_dirs_sorted %}
<li><a href="/{{subfile2.path|e}}">{{subfile2.name|e}}</a></li>
{% endfor %}
</ul>
<div id="clear"/>

Files
<table>
{% for subfile in file.listing() %}
<tr>
<td>{{subfile.type_letter()}}</td>
<td><a href="/{{subfile.path}}">{{subfile.name}}</a></td>
</tr>
{% endfor %}
</table>
"""

##############################################################################
## Page

_page_render_tmpl = """
<html>
<head>
<title>{{title}}</title>

<style type="text/css">
{{css_text}}
</style>

</head>
<body>
{{content}}
{{content_debug}}
</body>
</html>
"""

##############################################################################
## App

class File(object):
  
  def __init__(self,system,root,path):
    self.system = system
    abspath = os.path.join(root,path)
    self.realpath = abspath
    st = os.stat(abspath)
    self.path = path
    self.root = root
    if path == "":
      self.name = "/"
    else:
      self.name = os.path.basename(path)
    self.size = st.st_size
    self.mtime = st.st_mtime
    self.type_text = "Unknown file"

  def is_dir(self):
    return False

  def is_reqular(self):
    return False
  
  def type_letter(self):
    return "U"

class Reqular(File):
  
  def __init__(self,system,root,path):
    File.__init__(self,system,root,path)
    self.type_text = "Regular file"

  def is_reqular(self):
    return True

  def type_letter(self):
    return "R"


class Directory(File):
  
  def __init__(self,system,root,path):
    File.__init__(self,system,root,path)
    self.type_text = "Directory"

  def is_dir(self):
    return True

  def type_letter(self):
    return "D"
  
  def listing(self):
    rv = list()
    for name in os.listdir(unicode(self.realpath)):
      path_spec = os.path.join(self.path,name)
      try:
        file = self.system.create_file(path_spec)
      except OSError,e:
        log.error(str(e))
        continue
      rv.append(file)
    return rv

class Filebrowser(object):
  
  def __init__(self):
    self.root = "/home/hevi"
    self.session = session.Session()
    self.reg_render_tmpl = jinja.from_string(_reg_render_tmpl)
    self.dir_render_tmpl = jinja.from_string(_dir_render_tmpl)
    self.page_render_tmpl = jinja.from_string(_page_render_tmpl)
  
  def __call__(self,environ,start_response):
    fields = parse_formvars(environ)
    start_response('200 OK', [('content-type', 'text/html')])
    try:      
      log.debug("PATH_INFO " + environ["PATH_INFO"])
      file = self.create_file(environ["PATH_INFO"])
      title = "A title"
      if file.is_dir():
        content = self.render_dir(file)
      else:
        content = self.render_reg(file)
    except OSError,e:
      content = "Error " + str(e)
      title = content
    content_debug = "<hr/>\nNo debugging"
    css_text = _css_text
    stream = self.page_render_tmpl.stream(vars())
    return stream

  def render_dir(self,file):
    list_all = file.listing()
    list_dirs_sorted = list()
    list_nondirs_sorted = list()
    list_dirs_hidden = list() # sorted
    list_nondirs_hidden = list() # sorted
    for file1 in list_all:
      if self.is_hidden_file(file1):
        if file1.is_dir():
          list_dirs_hidden.append(file1)
        else:
          list_nondirs_hidden.append(file1)        
      else:      
        if file1.is_dir():
          list_dirs_sorted.append(file1)
        else:
          list_nondirs_sorted.append(file1)
    list_dirs_sorted.sort(lambda a,b: cmp(a.name,b.name))
    list_nondirs_sorted.sort(lambda a,b: cmp(a.name,b.name))    
    list_dirs_hidden.sort(lambda a,b: cmp(a.name,b.name))
    list_nondirs_hidden.sort(lambda a,b: cmp(a.name,b.name))    
    content = self.dir_render_tmpl.render(vars())
    return content

  def is_hidden_file(self,file):
    for pattern in self.session.hidden_files():
      if fnmatch.fnmatch(file.name,pattern):
        return True
    return False
    
  def render_reg(self,file):
    content = self.reg_render_tmpl.render(vars())
    return content

  def create_file(self,path_info):
    """
    PATH_INFO starts with root "/".
    @param path_info Path specification from wsgi PATH_INFO variable. 
    """
    path = path_info
    if path[0] == "/":
      path = path[1:] # strip "/" away
    real_path = os.path.join(self.root,path)
    if os.path.isdir(real_path):
      log.debug("new directory " + real_path)
      file = Directory(self,self.root,path)
    else:
      log.debug("new directory " + real_path)
      file = Reqular(self,self.root,path)
    return file 
    


##############################################################################
## Run

def run():
  ##
  log.debug("FS encoding: " + sys.getfilesystemencoding())
  ##
  host = "localhost"
  port = 12345
  app = Filebrowser()
  ##
  url = "http://%(host)s:%(port)d/" % vars()
  log.info("open: %(url)s" % vars())
  browser = wb.get('firefox')
  browser.open(url)
  ##
  log.info("running server forever ..")
  pserver.serve(app,host=host,port=port,threadpool_workers=5)
  
  
if __name__ == '__main__':
  logging.basicConfig()
  logging.getLogger().setLevel(logging.DEBUG)
  run()
  