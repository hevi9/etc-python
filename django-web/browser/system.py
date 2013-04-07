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
import sys
import os
import time
import logging
log = logging.getLogger(__name__)
import mimetypes
try:
  import magic
except:
  magic = None
import hevi_sys.control as huc
from hevi_util.common import *

#############################################################################
## File

class File(object):
  def __init__(self,root,relpath):
    self._root = root
    self._relpath = relpath
    self._update_time = 0
    self._stat_obj = None # stat object
    
  def name(self):
    return os.path.basename(self._relpath)

  def size(self):
    self.update()
    return self._stat_obj.st_size
  
  def mtime(self):
    self.update()
    return self._stat_obj.st_mtime
  
  def ftype_str(self):
    s = System()
    return s.ftype_str(self)
      
  def is_dir(self):
    return os.path.isdir(self.abspath()) 

  def is_reg(self):
    return os.path.isfile(self.abspath()) 
  
  
  ##
  def abspath(self):
    return os.path.join(self._root,self._relpath)

  def relpath(self):
    return self._relpath
  
  def root(self):
    return self._root

  ##
  def update(self):
    now = time.time()
    if self._update_time + self.reactivity() > now:
      return
    ## fill values
    self._update_time = now
    self._stat_obj = os.lstat(self.abspath())
    
  def reactivity(self):
    return 60 # min

#############################################################################
## Reg

class Reg(File):
  def __init__(self,root,relpath):
    super(Reg,self).__init__(root,relpath)

#############################################################################
## Dir

class Dir(File):
  def __init__(self,root,relpath):
    super(Dir,self).__init__(root,relpath)
    self._files = None
    
  def content(self):
    """
    return list of file
    """
    self.update()
    return self._files

  def update(self):
    now = time.time()
    if self._update_time + self.reactivity() > now:
      return
    super(Dir,self).update()
    ##
    if not os.access(self.abspath(), os.R_OK):
      return
    lof = list()
    for name in os.listdir(self.abspath()):
      abspath = os.path.join(self.abspath(),name)
      if(os.path.isdir(abspath)):
        file = Dir(self._root,os.path.join(self._relpath,name))
      else:
        file = Reg(self._root,os.path.join(self._relpath,name))
      lof.append(file)
    self._files = lof
    
#############################################################################
## System    

class System(Singleton):
  def __init__(self):
    self._root = os.environ["HOME"];
    ##
    self._magic = None
    if magic:
      self._magic = magic.open(magic.MAGIC_NONE)
      self._magic.load()
    
  def get_file(self,path):
    abspath = os.path.join(self._root,path)
    if not os.path.exists(abspath):
      raise NameError(abspath)
    if os.path.isdir(abspath):
      return Dir(self._root,path)
    else:
      return Reg(self._root,path)
    
  def ftype_str(self,afile):
    if afile.is_dir():
      return "directory"
    type_tup = mimetypes.guess_type(afile.abspath())
    if not type_tup[0] is None:
      return type_tup[0]
    if self._magic:
      type_x = self._magic.file(afile.abspath())
      return str(type_x)
    else:
      return "RAW"
    
    
    
