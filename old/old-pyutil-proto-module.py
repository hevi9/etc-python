#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id$
## MODULE

assert False,"Not for use"

"""
TODO: migrate from pytils/module
"""
__version__ = "$Revision$"
__docformat__ = "plaintext"

######################################################################
## dependencies

#import sys
import os
import sys
import re
import imp
import logging as log
from pyutil.script import Path,Script
log = log.getLogger("pyutil.module")

######################################################################
##

anon_count = 1    

def import_anon_file(file):
  """ TODO: validate """
  global anon_count
  fd = open(file)
  log.debug("importing %s anonymoysly as %s" % (file,"anon"+str(anon_count)))
  module = imp.load_module("anon" + str(anon_count),fd,file,
    imp.get_suffixes()[2])
  anon_count += 1
  fd.close()
  return module
  
def import_named_file(file):
  """ TODO: implement """
  file = Path(file)
  dir,name,ext = file.dir_base_ext(nodot=True)
  if dir in sys.path:
    #print dir
    pass

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

