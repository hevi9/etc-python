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

import hevi_misc.ttree_gear.builder_file as bl1
import hevi_misc.ttree_gear.builder_filetag as bl2


##############################################################################
## App

class App(object):
  def __init__(self):
    self.on_init()
    
  def on_init(self):
    log.debug("App.on_init")
    ## setup jinja
    self._tmplenv = jinja2.Environment(loader=jinja2.PackageLoader(
     "hevi_misc","ttree_gear"))
    self._ctx = dict()
    self._ctx["title"] = "Tree"
    ## Tree
    self.tree = tt.Tree()
    rl = "/home/hevi/wrk"
    ## setup and run builders
    self.builder = bl1.FileBuilder(self.tree,rl)
    self.builder.start()
    self.builder2 = bl2.TagFileBuilder(self.tree)
    self.builder2.start()
    ##
    self._ctx["tree"] = self.tree
    self._ctx["entries"] = self.tree.entries()
    ##
    log.debug("App.on_init: Tree: %d entries" % len(self.tree.index()))
  
  def on_shutdown(self):
    log.debug("App.on_shutdown")

  def __call__(self,environ,start_response):
    fields = parse_formvars(environ)
    start_response('200 OK', [('content-type', 'text/html')])
    self._ctx["title"] = "Request"
    self._ctx["fields"] = fields
    self._ctx["environ"] = environ
    ## 
    req_path = environ["PATH_INFO"]
    ## 1. resolve entry
    entry = self.resolve_entry(req_path)
    
    
    ## 2. resolve action
    ## 3. process action (with wsgi iteration)
    
    #action = self.find_action(req_path,environ)
    action = Action(self)
    ## Render
    apage = action.page_template()
    return apage.render(self._ctx)
    # return action.process()

  def resolve_entry(self,path_req):
    """ """
    ## absolute paths
    ## relative paths ? 
    log.debug("request path: " + path_req)


  def find_action(self,req_path,environ):
    ## Dispatch
    ##  *type*(entry) => action(entry) 
    pass

  def tmplenv(self):
    return self._tmplenv

    
    

##############################################################################
## Action

class Action(object):
  ## processing the action
  ## only one action instance by default
  ## => one process method
  """ """
  def __init__(self,app):
    """ """
    self._app = app
    
  def name(self):
    return "test"
  
  def process(self,entry,environ,start_response):
    """
    @return: wsgi iterable
    @rtype: string iterable
    """
  
  def page_template(self): # process
    return self._app.tmplenv().get_template("page_all_entries.html")
    


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
  