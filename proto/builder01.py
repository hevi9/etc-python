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
from hevi_util.common import *
from hevi_misc.tagtree import *

##############################################################################
## Tree Builder

class Builder(object):

  def __init__(self,tree):
    self._tree = tree
    self._progress_chars = 0

  def build_in_dir(self,rl):
    """  """
    tree = self._tree
    tree.update_begin()
    ##
    for name in os.listdir(rl):
      if self.is_ignored(name):
        continue
      abspath = os.path.join(rl,name)
      for root, dirs, files in os.walk(abspath):
        f = self.create_file(root,rl)
        tree.insert(f)
        f.tags_set("dir")
        self.progress("d")
        for dir in dirs:
          if self.is_ignored(dir):
            dirs.remove(dir)
        for file in files:
          if self.is_ignored(file):
            continue
          f = self.create_file(os.path.join(root,file),rl)
          tree.insert(f)
          f.tags_set("file")
          self.progress("f")
    ##
    self.progress(" %d files\n" % len(tree.files()))
    tree.update_end()

  def create_file(self,path_abs,root):
    f = File()
    f.tree(self._tree)
    f.path_abs(path_abs)
    f.path_root(root)
    #print path_abs
    #print root
    #print os.path.relpath(path_abs, root)
    return f

  def progress(self,txt):
    return
    if self._progress_chars > 77:
      sys.stdout.write("\n")
      self._progress_chars = 0      
    sys.stdout.write(txt)
    sys.stdout.flush()
    self._progress_chars += len(txt)
    
  def is_ignored(self,filename):
    ignored = [".svn",".metadata",".settings"
    ]
    if filename in ignored:
      return True
    return False
  

##############################################################################
## Tree Builder

class TagBuilder(object):

  def __init__(self,tree):
    self._tree = tree

  def start(self):
    self.run()
    
  def run(self):
    tree = self._tree
    tree.update_begin()
    ## path tags
    for entry in tree.entries():
      for tag in entry.path().split(os.sep)[:-1]:
        entry.tags_set(tag)
    ## extension tags
    for entry in tree.entries():
      ext = os.path.splitext(entry.path())[1]
      if ext == '':
        continue
      if ext[0] == '.':
        ext = ext[1:]
      entry.tags_set(ext)

    ##
    tags = Group()
    tags.tree(tree)
    tags.path("__tags__")
    tree.insert(tags)
    Group(tree,"__tags__")
    ##
    tree.update_end()
    

