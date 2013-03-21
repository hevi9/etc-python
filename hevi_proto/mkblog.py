"""
Blog composer and publisher
===========================

Usage::

 > mkblog

"""

import os # http://docs.python.org/3/library/os
import fnmatch # http://docs.python.org/3/library/fnmatch
import logging # # http://docs.python.org/3/library/os
from docutils.parsers.rst import Parser
from docutils.utils import new_document
from docutils import frontend
log = logging.getLogger(__name__)

class cfg:
  root = os.getcwd()
  include = [ "*.rst" ]
  ignore = [ "README.rst" ]

def collect():
  rfiles = list()
  for top, dirs, files in os.walk(cfg.root):
    ## remove ignores from files and dirs
    for file in files:
      for match in cfg.ignore:
        if fnmatch.fnmatch(file, match):
          files.remove(file)
    for dir in dirs:
      for match in cfg.ignore:
        if fnmatch.fnmatch(dir, match):
          files.remove(dir)
    ## collect
    for file in files:
      for match in cfg.include:
        if fnmatch.fnmatch(file, match):
          rfiles.append(os.path.join(top,file))
  return rfiles

def parse(files):
  #log.debug(files)
  documents = list()
  parser = Parser()
  settings = frontend.OptionParser().get_default_values()
  settings.tab_width = 2
  settings.pep_references = True
  settings.rfc_references = True
  for file in files:
    with open(file) as fd:
      text = fd.read()
    document = new_document(file,settings)
    parser.parse(text, document)
    documents.append(document)
  return documents

def publish(arg):
  pass

def main():
  logging.basicConfig(level=logging.DEBUG)
  log.info("cfg.root={}".format(cfg.root))
  
  #publish(format(collect()))
  log.debug(parse(collect()))

if __name__ == "__main__": main()