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
#from stat import *
#import mimetypes as mt
import time
import logging
log = logging.getLogger(__name__)
from hevi_util.common import *
import hevi_misc.tagtree as tt

##############################################################################
## Tag File Builder

class TagFileBuilder(tt.Builder):
  """  """

  def __init__(self,tree):
    """
    """
    super(TagFileBuilder,self).__init__(tree)

  def run(self):
    for entry in self._tree.index().values():
      if not isinstance(entry,tt.FileBase):
        continue
      self.tag_time(entry)
      self.tag_size(entry)
      self.tag_bypath(entry)

  def tag_time(self,entry):
    tm = time.localtime(entry.mtime())
    entry.tag_insert(str(tm.tm_year))
    entry.tag_insert(time.strftime("%b",tm))

  def tag_size(self,entry):
    if entry.size() >= (1024 * 1024):
      entry.tag_insert("mega") 

  def tag_bypath(self,entry):
    for part in entry.path().split(self._tree.sep())[:-1]:
      entry.tag_insert(part)
  
