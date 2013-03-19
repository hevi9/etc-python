#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" 
Test for pyild. 
"""

##############################################################################
## Uses & Setup

import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import unittest # http://docs.python.org/py3k/library/unittest.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
from hevi_proto.pyild import main

#############################################################################
## Test 

pyildfile = """
from hevi_proto.pyild import task

@task
def clean():
  print("clean A")

@task("pre1")
def setup():
  print("setup A")

@task("setup")
def clean():
  print("clean B")

@task
def clean():
  print("clean C")

@task
def pre1():
  print("pre1")
  
"""

class TestPropsDict(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    with open("pyildfile","w") as fd:
      fd.write(pyildfile)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
    os.remove("pyildfile")

  def test_pyild(self):
    main()
        
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()
