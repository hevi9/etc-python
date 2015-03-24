#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: test_run_01.py,v 1.1 2005-02-22 15:51:20 hevi Exp $
## UNITTEST

"""
"""

######################################################################
## dependencies

import unittest
import os

######################################################################
## dependencies

import logging as log
from pyutil.globals import *

######################################################################
## which

def which(name,**kwds):
  """
  name as str.
  keywords:
    envvar as str by default "PATH".
    sep as str by default ":".
    need_exec as boolean by default True.
  return file:
    file as Path or None
  """
  ## set config
  need_exec = kwds.get("need_exec",True)
  envvar = kwds.get("envvar","PATH")
  #print ">>>",envvar
  sep    = kwds.get("sep",":")
  ##
  name = Path(name)
  ##
  file = None
  if name.is_uniq():
    file = name
  else:
    try:
      for dir in os.environ.get(envvar).split(sep):
        dir = Path(dir).uniq_path()
        file = dir / name
        if file.exists():
          break # found
        file = None
    except KeyError,e: # no envvar to search from
      log.debug(str(e))
      return None
  ##
  if file == None:
    log.debug("%s not found" % name)
    return None
  if not file.is_reg():
    log.debug("%s is not regular" % file)
    return None
  if need_exec and not file.can_exec():
    log.debug("%s exits but does not has execute access" % file)
    return None
  return file

######################################################################
## Program

class Program(object):
  
  def __init__(self,name_or_program,*base_args,**kwds):
    """
    name_or_program as str or Program.
    args as str.
    kwds:
    """
    
    def exists(self):
      """
      out: exists as boolean.
      """
    
class Programs(object):
  """ Set of programs providing same functionality.
  Select first found.
  """
  def __init__(self,*programs,**kwds):
    """
    """
    
######################################################################
## test config

test_root = Path("/tmp")
    
######################################################################
## test utils

j = os.path.join

def make_dir_join(*args):
  dir = os.path.join(*args)
  if not os.path.exists(dir):
    log.debug("making %s",dir)
    os.makedirs(dir)
  return dir

def make_exec_file_join(*args):
  file = os.path.join(*args)
  dir = make_dir_join(os.path.dirname(file))
  fd = open(file,"w")
  fd.write('#!/bin/sh\n')
  fd.write('/bin/true\n')
  fd.close()
  os.chmod(file,0755)
  return file

def make_regu_file_join(*args):
  file = os.path.join(*args)
  dir = make_dir_join(os.path.dirname(file))
  fd = open(file,"w")
  fd.write('TEXT\n')
  fd.close()
  os.chmod(file,0644)
  return file
  

######################################################################
## tests

class TestProgram(unittest.TestCase):

  def test_Func(self):
    """ test functionality """
    assert(1)

######################################################################
## test which

class Test_which(unittest.TestCase):

  def setUp(self):
    ##
    self.root = os.tmpnam()
    self.dira = make_dir_join(self.root,"dira")
    self.dirb = make_dir_join(self.root,"dirb")
    self.dirc = make_dir_join(self.root,"dirc")    
    self.execa = make_exec_file_join(self.dira,"execa")
    self.execb = make_exec_file_join(self.dirb,"execb")
    self.execc = make_exec_file_join(self.dirc,"execc")
    self.regua = make_exec_file_join(self.dira,"regua")
    self.regub = make_exec_file_join(self.dirb,"regub")
    self.reguc = make_exec_file_join(self.dirc,"reguc")
    
  def tearDown(self):
    log.debug("removing %s",self.root)    
    for root, dirs, files in os.walk(self.root, topdown=False):
      for name in files:
        os.remove(os.path.join(root, name))
      for name in dirs:
        os.rmdir(os.path.join(root, name))
    os.rmdir(self.root)

  def test_which_envvar_default(self):
    """  """
    os.environ["PATH"] = os.environ["PATH"] + ":" + ":".join(
      [self.dira,self.dirb,self.dirc])
    found = which("execb")
    assert found == j(self.root,"dirb","execb")

  def test_which_envvar_set(self):
    """  """
    os.environ["SOMEPATH"] = ":".join([self.dira,self.dirb,self.dirc])
    found = which("execb",envvar="SOMEPATH")
    assert found == j(self.root,"dirb","execb")

  def test_which_sep_set(self):
    """  """
    assert(1)
    os.environ["SOMEPATH"] = ";".join([self.dira,self.dirb,self.dirc])
    found = which("execb",envvar="SOMEPATH",sep=";")
    assert found == j(self.root,"dirb","execb")

  def test_which_need_exec_set(self):
    """ Find regular file  """
    os.environ["SOMEPATH"] = ":".join([self.dira,self.dirb,self.dirc])
    found = which("regub",envvar="SOMEPATH",need_exec=False)
    assert found == j(self.root,"dirb","regub")


######################################################################
## running

if __name__ == '__main__':
  log.basicConfig()
  #log.getLogger().setLevel(log.DEBUG)  
  unittest.main()

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
