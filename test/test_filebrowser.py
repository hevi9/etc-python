#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
__tags__      = "test"
""" filebrowser tests """

##############################################################################
## Uses

import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import unittest # http://docs.python.org/py3k/library/unittest.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)

from filebrowser01 import *

##############################################################################   
## Test base

class TestBase(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)

#############################################################################
## Test Thing

class test_filebrowser(TestBase):

  def test_make_rplist(self):
    """ rplist """
    print(make_rplist("/"))
    print(make_rplist("/home"))
    print(make_rplist("/home/hevi"))

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
