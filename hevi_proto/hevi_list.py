#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: pse-list.py,v 1.3 2006-02-21 14:50:08 hevi Exp $

################################################################################
import os
import sys

################################################################################

# remember "," at end, if only one suffix
typemap = (
  # suffixes      , cmd,      options
  ((".tgz",".tar.gz"),"tar",    "tzvf"),
  ((".tar.bz2",),      "tar",    "tjvf"),
  ((".zip",),       "unzip",    "-l"),
  ((".deb",),       "dpkg-deb", "--contents")
)

class File(object):
  def should_handle(self,path):
    return False
  def list(self,path):
    raise NotImplementedError
    
class Reg(File):

  def should_handle(self,path):
    return True

  def list(self,path):
    cmd = "less"
    options = "-M" # long prompt
    cmdline = "%(cmd)s %(options)s %(path)s" % vars()
    os.system(cmdline)
  
class Dir(File):

  def should_handle(self,path):
    return os.path.isdir(path)

  def list(self,path):
    cmd = "ls"
    options = "-lLF" # long format, deference symlink,classify
    cmdline = "%(cmd)s %(options)s %(path)s" % vars()
    os.system(cmdline)

class FileExt(File):

  def __init__(self,suffixes,cmd,options):
    self._suffixes = suffixes
    self._cmd = cmd
    self._options = options

  def should_handle(self,path):
    for suffix in self._suffixes:
      if path.endswith(suffix):
        return True
    return False

  def list(self,path):
    cmd = self._cmd
    options = self._options
    cmdline = "%(cmd)s %(options)s %(path)s" % vars()
    os.system(cmdline)

  
################################################################################

class Main(object):

  def __init__(self):
    self._handlers = list()
    self._handlers_init()

  def run(self):
    args = sys.argv[1:]
    if len(args) == 0:
      args.append(".")
    for arg in args:
      handler = self._resolve_handler(arg)      
      handler.list(arg)
    
  def _handlers_init(self):
    self._handlers.append(Dir())    
    for mapping in typemap:
      self._handlers.append(FileExt(*mapping))
    self._handlers.append(Reg())


  def _resolve_handler(self,path):
    for handler in self._handlers:
      if handler.should_handle(path):
        return handler
    return None

################################################################################
if __name__ == '__main__':
  Main().run()

################################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
