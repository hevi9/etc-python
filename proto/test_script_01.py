#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__      = "test"
__version__   = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__   = "$Release$"
__docformat__ = "epytext"
"""
See also http://docs.python.org/library/unittest.html .
"""

##############################################################################
## Uses

import sys
import os
import unittest
import logging
log = logging.getLogger(__name__)

##############################################################################
## Test configuration

from hevi_util.script import * # protp = hevi_util


##############################################################################
## Test material

##############################################################################   
## Test base

class TestBase(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)

#############################################################################
## Test Thing

class test_script(TestBase):

  def test_mkdir(self):
    """ mkdir """
    mkdir("/tmp/a")

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
