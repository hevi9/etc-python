#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__    = "proto"
__version__ = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__ = "$Release$"
__docformat__ = "epytext"
"""
"""

##############################################################################
## Uses

import sys
import os
import logging
log = logging.getLogger(__name__)
import unittest
from hevi_util.common import *

##############################################################################
## Proto

class File(object):
  def __init__(self):
    self._path_abs = None
    self._path_root = None
    
  def path_abs(self,value = Void):
    """
    """
    if value is not Void:
      self._path_abs = value
    return self._path_abs

  def path_root(self,value = Void):
    """
    """
    if value is not Void:
      self._path_root = value
    return self._path_root

  def path_rel(self):
    return os.path.relpath(self._path_abs, self._path_root)

class Tree(object):
  def __init__(self):
    self._files = dict()
  
  def files(self):
    return self._files
  
  def insert(self,file):
    self._files[file.path_rel()] = file

##############################################################################
## Proto usage

class test_Proto(unittest.TestCase):
  
  def test_usage(self):
    """ usage """
    #log.debug("some usage")
    tree = Tree()
    rl = "/home/hevi/wrk"
    ##
    for name in os.listdir(rl):
      abspath = os.path.join(rl,name)
      #print name
      for root, dirs, files in os.walk(abspath):
        #print "  D ", root
        f = self.create_file(root,rl)
        tree.insert(f)
        print "d"
        for file in files:
          #print "   F ",os.path.join(root,file)
          f = self.create_file(os.path.join(root,file),rl)
          tree.insert(f)
          print "f"
    ##
    print len(tree.files())

  def create_file(self,path_abs,root):
    f = File()
    f.path_abs(path_abs)
    f.path_root(root)
    #print path_abs
    #print root
    #print os.path.relpath(path_abs, root)
    return f

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
