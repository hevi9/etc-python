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

##############################################################################
## Proto

##############################################################################
## Proto usage

class test_Proto(unittest.TestCase):
  
  def test_usage(self):
    """ usage """
    log.debug("some usage")
    r = d("/tmp/filemakertest")
    r.f("file1",copy,"/tmp/joo")
    r.l("link2","/home/jee")

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
