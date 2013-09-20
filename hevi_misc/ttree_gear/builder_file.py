#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__    = "proto"
__version__ = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__ = "$Release$"
__docformat__ = "epytext"
"""
Need recursive walk, os.walk is too hard to get right for hierarchical
tree filling, eg. group in group.
"""

##############################################################################
## Uses

import sys
import os
from stat import *
import mimetypes as mt
import time
import logging
log = logging.getLogger(__name__)
from hevi_util.common import *
import hevi_misc.tagtree as tt

##############################################################################
## File Builder

class FileBuilder(tt.Builder):
  """ Build file system tree into tree. """

  def __init__(self,tree,path_root):
    """
    @param path_root: Root directory where to build. Root dir is not included. 
    """
    super(FileBuilder,self).__init__(tree)
    # require path_root is directory
    assert os.path.isdir(path_root)
    self._path_root = path_root

  def run(self):
    for fname in os.listdir(self._path_root):
      abspath = os.path.join(self._path_root,fname)
      self._traverse(fname, abspath,self._tree)

  def _traverse(self,top_name,top_abs_path,top_group):
    if self.is_ignored(top_name):
      self.log_ignored(top_abs_path)
      return
    try:
      st = os.stat(top_abs_path)
    except OSError,e:
      self.log_ignored(top_abs_path)
      log.warn(str(e))
      return
    if S_ISDIR(st.st_mode):
      group = self.make_dir(top_group,top_name,top_abs_path,st)
      try:
        for name in os.listdir(top_abs_path):
          abs_path = os.path.join(top_abs_path,name)
          self._traverse(name, abs_path, group)
      except OSError,e:
        self.log_ignored(top_abs_path)
        log.warn(str(e))
        return        
    elif S_ISREG(st.st_mode):
      self.make_file(top_group,top_name,top_abs_path,st)
    else:
      self.log_ignored(top_abs_path)
       
  def make_file(self,in_group,name,path_abs,stinfo):
    #print " F",path_abs,in_group
    file = tt.File(in_group,name,path_abs,self._path_root,stinfo)
    type_mime,encoding = mt.guess_type(path_abs)
    if type_mime is not None:
      file.type_mime(type_mime)
    return file

  def make_dir(self,in_group,name,path_abs,stinfo):
    #print "D",path_abs,in_group
    dir = tt.Dir(in_group,name,path_abs,self._path_root,stinfo)
    return dir
      
  def is_ignored(self,filename):
    ignored = [".svn",".metadata",".settings"
    ]
    if filename in ignored:
      return True
    return False
  
  def log_ignored(self,path_abs):
    #print "I",path_abs
    pass

