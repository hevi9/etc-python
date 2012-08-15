#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2010 Petri Heinilä, License LGPL 2.1
""" Web content creation utilities. 

Usage::

   from hevi_web.web import *
   web = Web(root)
   page1 = web.page(path)
   page2 = web.page(path)
   web.render_all()
  
   OR
  
   dynamic
  
"""

##############################################################################
## Uses
import sys
import os
j = os.path.join
import logging
log = logging.getLogger(__name__)
import jinja2
import platform
import datetime

import hevi_web # needed for __path__ resources

__all__ = list()

#############################################################################
## Book

class Book:
  """ general collection and mediator object for a site. """
  def __init__(self,**kwds):
    """
    @keyword viewcache: Directory to build html view cache.
    """
    ##
    self.root_style = j(hevi_web.__path__[0],"style")
    log.debug("Book.root_style = " + self.root_style)
    ##
    self.use_style = "fallback"
    self.dir_style = j(self.root_style, self.use_style)
    log.debug("Book.use_style = " + self.use_style)
    log.debug("Book.dir_style = " + self.dir_style)
    ##
    self.dir_viewcache_root = kwds.get_default("viewcache","/tmp/viewcache")
    log.debug("Book.viewcache_root = " + self.viewcache_root)
    ##
    self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.dir_style))
    ## 
    
    
__all__.append("Book")

#############################################################################
## Page
  
class Page:
  def __init__(self,book,title,genfunc):
    """
    """
    self._book = book
    self._title = title
    self._genfunc = genfunc
    
  def run(self):
    self._genfunc(self)
    
  def rurl(self):
    """ Relative url. """
    
  def mangle(self):
    """ Mangle title to the name or filename.
    If not allowed char => "_"
    """
    wrk = self._title
    wrk = wrk.strip().lower()
    last_ch = None
    tmp = ""
    for ch in wrk:
      #log.debug(str(ord(ch)))
      if (ch == "-" or 
          ch == "_" or 
          (ord(ch) >= ord("a") and ord(ch) <= ord("z")) or
          (ord(ch) >= ord("0") and ord(ch) <= ord("9"))
          ):  
        tmp += ch
        last_ch = ch        
      else:
        if last_ch != "_":
          tmp += "_"
        last_ch = "_"
    wrk = tmp.strip("_")    
    return wrk

  def get_base_ctx(self):
    return {
            "page" : {
                      "title": platform.node(),
                      "gentime": datetime.datetime.now().isoformat(),
                      }
            }
__all__.append("Page")
