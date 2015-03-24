#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2008 Petri Heinilä, License LGPL 2.1
__tags__      = "module"
__version__   = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__   = "$Release$"
__docformat__ = "epytext"
"""
"""

##############################################################################
## Uses

import os
import logging
log = logging.getLogger(__name__)
import fnmatch
import mimetypes
import jinja2
import hevi_util.main as hum
import hevi_util.fileops
fs = hevi_util.fileops.default()
import hevi_sys.control as control
U = unicode
j = os.path.join

##############################################################################
## Item

class Item(object):
  def __init__(self):
    pass

##############################################################################
## Error

class Error(object):
  def __init__(self,exception):
    super(Error,self).__init__()
    self.exception = exception

##############################################################################
## FileItem

class FileItem(Item):
  def __init__(self,root,pathl):
    super(FileItem,self).__init__()
    self.root = U(root)
    self.pathl = pathl

  def abs_file(self):
    pathl = self.pathl
    return j(self.root,*pathl)

  def update(self):
    """ Update item information from resource. """

##############################################################################
## File

class File(FileItem):
  def __init__(self,root,pathl):
    super(File,self).__init__(root,pathl)
    
  def update(self):
    st = os.stat(self.abs_file())
    self.size = st.st_size
    mimetype,enc = mimetypes.guess_type(self.abs_file())
    self.mimetype = mimetype 
    
##############################################################################
## Dir

class Dir(FileItem):
  def __init__(self,root,pathl):
    super(Dir,self).__init__(root,pathl)

  def update(self):
    pass

##############################################################################
## Gear

class Gear(FileItem):
  def __init__(self,root,pathl):
    super(Gear,self).__init__(root,pathl)

##############################################################################
## Template
## index template
## foreach file template
## subtemplate template
## image
## needed ?

class Page(FileItem):
  def __init__(self,**kwds):
    """
    @keyword builder:
    @keyword template:
    @keyword title:   
    @keyword root:
    @keyword pathl:  
    """
    super(Page,self).__init__(kwds["root"],kwds["pathl"])
    self.builder = kwds.get("builder",None)
    assert self.builder
    self.template = kwds.get("template",None)
    assert self.template
    self.title = kwds.get("title",None)
    assert self.title
    #log.debug("page: " + self.abs_file()) 

  def render(self):
    ctx = self.builder.context()
    ctx["page"] = self.__dict__
    log.debug("writing: " + self.abs_file())
    self.template.stream(ctx).dump(self.abs_file())
      
  def rel_url(self):
    """ Relative url from output root to access this page.
    """

##############################################################################
## Build Source 

j = os.path.join

class BuildSource(hum.Main):
  def __init__(self,*args,**kwds):
    ctrl = control.Control()
    super(BuildSource,self).__init__(debug=True,title="Build Source Code")
    self._roots = [ctrl.get("wrk_dir"),"/tmp/test"]
    self._output_dir = j(ctrl.get("public_html_dir"),"source")
    self._exclude_names = [".svn",".settings",".workspace",".metadata",
                           ".project",".pydevproject","CVS","*.pyc"]
    self._template_dir = j(ctrl.get("hevi_sys_dir"),"data","hevi_build_code")
    self._templates = list()
    ##
    self.items = list()
    self.errors = list()
    self.files = list()
    self.top_templates = list()
    self.gears = list()
    self.jenv = jinja2.Environment(
      loader=jinja2.FileSystemLoader(U(self._template_dir)))
    self.pages = list()
    self._context = None
    self.tree = None # directory tree
    ##
    mimetypes.init()
  
  def run(self):
    log.info(" ".join(map(str,self._roots)) + " => " + str(self._output_dir))
    ##
    self._collect_files()
    log.debug("files: %d, errors %d" % (len(self.files),len(self.errors)))
    ##
    self._collect_templates()
    log.debug("top templates: %d, gears %d" % 
     (len(self.top_templates),len(self.gears)))
    ## build pages
    self._build()
    log.debug("pages: %d" % (len(self.pages)))
    ## generate pages to files
    self._generate()
    
  def _collect_files(self):
    for root in self._roots:
      log.debug("" + str(root))
      for top,dirs,files in os.walk(str(root),topdown=True,onerror=self._add_file_error):
        ## exclude directories, affects also to walking
        for pat in self._exclude_names:
          for name in fnmatch.filter(dirs, pat):
            dirs.remove(name)            
        ## exclude files
        for pat in self._exclude_names:
          for name in fnmatch.filter(files, pat):
            files.remove(name)
        for file1 in files:              
          l = len(str(root).split(os.sep))
          pathl = top.split(os.sep)[l:]
          pathl.append(file1)
          self._add_file(root,pathl)
          
  def _add_file(self,root,pathl):
    file = File(root,pathl)
    file.update()
    self.files.append(file)
            
  def _add_file_error(self,oserror):
    error = Error(oserror)
    self.errors.append(error)
    self.items.append(error)
    
  def _collect_templates(self):
    root = U(self._template_dir)
    templates = os.listdir(root)
    ## exclude files
    for pat in self._exclude_names:
      for name in fnmatch.filter(templates, pat):
        templates.remove(name)
    for template in templates:
      if fnmatch.fnmatch(template,"top-*"):
        self._add_top_template(root,template)
      else:
        self._add_gear(root,template)
    
  def _add_top_template(self,root,template):
    template1 = self.jenv.get_template(os.path.basename(template))
    self.top_templates.append(template1)
    
  def _add_gear(self,root,file):
    self.gears.append(Gear(root,[file]))
    
  def _generate(self):  
    for page in self.pages:
      fs.mkdir(os.path.dirname(page.abs_file()))
      page.render()
    for gear in self.gears:
      fs.link(gear.abs_file())
      
  def _build(self):
    root = U(self._output_dir)
    for tmpl in self.top_templates:
      ## remove top- from name
      name = tmpl.name[4:]
      self._add_page(Page(builder=self,
        template=tmpl,
        title=name,
        root=root,
        pathl=[name]))
    
  def _add_page(self,page):
    self.pages.append(page)

  def context(self):
    if self._context:
      return self._context
    self._context = {
      "files": self.files,
      "items": self.items,
      "errors": self.errors,
      "pages": self.pages,
      "tree": self.tree
    }
    return self._context

##############################################################################
## Running
  
if __name__ == "__main__":
  bs = BuildSource()
  #main = hum.Main(run=bs.run,debug=True,title="Build Source Code")
  bs.start()
  