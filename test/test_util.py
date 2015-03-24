#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" 
Test for util module. 
"""

##############################################################################
## Uses & Setup

import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import unittest # http://docs.python.org/py3k/library/unittest.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
from hevi_proto.util import PropsDict

##############################################################################   
## Test base

class TestBase(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)

#############################################################################
## Test PropsDict

class TestPropsDict:
  
  def __init__(self):
    self.objdata = "OBJVALUE"
    self.props = PropsDict(self)
  
  @property
  def data1(self):
    return "VALUE1"

  @property
  def data2(self):
    return "VALUE2"
  
class test_PropsDict(TestBase):

  def test_access(self):
    """ property access """
    test = TestPropsDict()
    assert test.props["data1"] == "VALUE1"
    assert test.props["data2"] == "VALUE2"

  def test_iteration(self):
    """ property iteration """
    test = TestPropsDict()
    keys = ["data1","data2"]
    for prop in test.props:
      assert prop in keys
      keys.remove(prop)
    assert len(keys) == 0
        
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
