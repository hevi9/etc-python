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
import hevi_sys.control as huc
from hevi_util.common import *
from hevi_util.file_tree import *
    
#############################################################################
## Stats   

def mib(n):
  return "%0.1fMiB" % (n / (1024.0*1024))

def kib(n):
  return "%0.1fKiB" % (n / (1024.0))


class Stats(Singleton):
  
  def __init__(self):
    self.tree = Tree(os.environ["HOME"]);

  def update(self):
    self.tree.update_wait()
    self.process()
    
  def process(self):
    tree = self.tree
    ##
    self.files_nro = len(self.tree.all_files_dict())
    ##
    sum = 0
    for file in tree.all_files():
      sum += file.size()
    self.files_size_sum = sum
    ##
    self.files_size_avg= 1.0 * self.files_size_sum / self.files_nro 
    ##
    self.newest_files = list(self.tree.all_files())
    self.newest_files.sort(lambda x,y: int(y.mtime_s()) - int(x.mtime_s()))
    self.newest_files = self.newest_files[:10]
    ##
    self.oldest_files = list(self.tree.all_files())
    self.oldest_files.sort(lambda x,y: int(x.mtime_s()) - int(y.mtime_s()))
    self.oldest_files = self.oldest_files[:10]
    ##
    self.biggest_files = list(self.tree.all_files())
    self.biggest_files.sort(lambda x,y: y.size() - x.size())
    self.biggest_files = self.biggest_files[:10]
  
