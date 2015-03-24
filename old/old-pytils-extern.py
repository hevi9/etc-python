#!/usr/bin/env python
## $Id: extern.py,v 1.8 2003-08-13 16:58:59 hevi Exp $

"""
External resource usage tracking.
"""
__version__ = "$Revision: 1.8 $"

from __future__ import generators

if __name__ == '__main__':
  import pytils.extern
  import sys
  pytils.extern.check()

######################################################################
## dependencies

from pytils.common import *
from pytils.log import log
import os


######################################################################
## which

def which(cmd):
  """
  """
  file = None
  if os.path.exists(cmd):
    file = cmd
  else:
    for dir in os.environ.get("PATH").split(":"):
      file = dir + "/" + cmd
      if os.path.exists(file):
        break
      file = None
  if file == None:
    log.debug(cmd,"not found")
    return None
  if not os.path.isfile(file):
    log.error(file,"is not file")
    return None
  if not os.access(file,os.X_OK):
    log.error(file,"exits but does not has execute access")
    return None
  return file

######################################################################
## externs

class extern(object):
  """
  """

  __metaclass__ = Singleton
  
  def __init__(self):
    self.programs = {}
    self.files = {}
  
  def programs(self):
    """
    XXXX
    """
    return self.programs

  def program(self,name,abspath = None):
    """
    """
    wanted = list()
    if type(name) == list or type(name) == tuple:
      wanted.extend(name)
    else:
      wanted.append(name)
    if abspath == None:
      for i in wanted:
        abspath = which(name)
        if abspath != None:
          break
    self.programs[name] = abspath
    return abspath

  def files(self):
    """
    """
    return self.files.keys()

  def file(self,path):
    """
    """
    self.files[path] = 1
    return path

  def valid(self):
    """
    """
    if None in self.programs.values():
      return 0
    return 1

extern = extern()

######################################################################
## provided options

class options(object):
  
  def option_uses(self,arg):
    """ Show external dependencies """
    programs = extern.programs
    for prog in programs:
      print " -",prog,"from",programs[prog]
    self.exit(0)


######################################################################

class _check_extern(object):

  def check_programs(self):
    raise NotImplementedError

  def check_program(self):
    raise NotImplementedError

  def check_files(self):
    raise NotImplementedError

  def check_file(self):
    raise NotImplementedError

  def check_valid(self):
    raise NotImplementedError

def check():
  return 0

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

