#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
Formats source code files into one html file.

Example:
> prog --in-root /home/user/src/python -in-match "*.py" --out-html /home/user/public_html/python.html 

"""
__version__ = "$Rev: 4084 $"

##############################################################################
## Uses

import sys
import os
import argparse # http://docs.python.org/py3k/library/argparse.html
import fnmatch # http://docs.python.org/py3k/library/fnmatch.html
import cgi
import logging
import pygments as pyg # http://pygments.org/docs/
import pygments.lexers as pygl
import pygments.formatters as pygf
log = logging.getLogger(__name__)
from hevi_util.common import *
from hevi_util.script import *

##############################################################################
## FormatTask

@export
class FormatTask:
  """
  cfg.in_root -- list of str as roots
  cfg.in_match -- list of str as fnmacthes
  cfg.out_html -- str as result html file
  """
  
  def __init__(self,cfg,ui):
    self.cfg = cfg
    self.ui = ui
    self.files = list()

  def begin(self):
    for d in self.cfg.in_root:
      if not os.path.isdir(d):
        self.ui.exit_help("{0} is not directory".format(d))
        
  def run(self):
    self.discover()
    mkdir(os.path.dirname(self.cfg.out_html))
    log.info("creating {0}".format(self.cfg.out_html))
    self.files.sort()
    fd = open(self.cfg.out_html,"w")
    self.format_files_pygments(fd)
    fd.close()
  
  def end(self):
    log.info("Done.")

  def discover(self):
    """ Discover files to format. """
    for d in self.cfg.in_root:
      log.info("discover in {0}".format(d))
      for root, dirs, files in os.walk(d):
        for match in self.cfg.in_match:
          for file in files:
            if fnmatch.fnmatch(file, match):
              afile = os.path.join(root,file)
              self.files.append(afile)
              #log.debug(afile)
    log.info("{0} files found".format(len(self.files)))
    
  def format_files_simple(self,fd):
    w = fd.write
    for file in self.files:
      w('<hr/><a href="file://{0}">{0}</a>\n'.format(file))
      w("<pre>\n")
      rfd = open(file)
      try:
        w(cgi.escape(rfd.read()))
      except UnicodeDecodeError as e:
        log.error(file + ": " + str(e))
      rfd.close()
      w("</pre>\n")
      
  def format_files_pygments(self,fd):
    w = fd.write
    formatter = pygf.HtmlFormatter(linenos=True,cssclass="source")
    w('<html>\n')
    w("<head>\n")
    w('<style type="text/css">\n')
    w(formatter.get_style_defs())    
    w("</style>\n")        
    w("</head>\n")        
    for file in self.files:
      log.debug(".. formatting {0}".format(file))
      w('<hr/><a href="file://{0}">{0}</a>\n'.format(file))
      lexer = pygl.get_lexer_for_filename(file,stripall=True)
      try:
        rfd = open(file)
        code = rfd.read()
        w(pyg.highlight(code, lexer, formatter))
        del code
      except UnicodeDecodeError as e:
        log.error(file + ": " + str(e))
      finally:              
        rfd.close()
    w("</html>\n")

    
    
    
##############################################################################
## UI

@export
class UI:
  def __init__(self):
    logging.basicConfig(level=logging.DEBUG)
  
  def exit_ok(self):
    sys.exit(0)
    
  def exit_error(self,msg):
    log.error(msg)
    sys.exit(1)
    
  def exit_help(self,msg):
    log.error(msg)
    sys.exit(2)    
    
@export
class CmdUI(UI):
  def __init__(self):
    super().__init__()
    self.parser = argparse.ArgumentParser(description=__doc__.strip())
    self.parser.add_argument("--in-root", nargs="+", metavar="ROOT", required=True,
                        help="Root where to search code files.")
    self.parser.add_argument("--in-match", nargs="+", metavar="MATCH", required=True,
                        help="Include these matched files to formatting, fnmatch")
    self.parser.add_argument("--out-html", metavar="FILE", required=True,
                        help="Result one html file")
    self.parser.add_argument('--version', action='version', 
                             version='%(prog)s ' + __version__)
    
  def parse(self):
    """ Returns cfg (args). """
    return self.parser.parse_args()    
    
  def exit_help(self,msg):
    log.error(msg)
    self.parser.print_help()
    sys.exit(2)        

##############################################################################
## Code

def run():
  ui = CmdUI()
  args = ui.parse()
  task = FormatTask(args,ui)
  task.begin()
  task.run()
  task.end()

##############################################################################
## Running
  
if __name__ == "__main__":
  run()
  