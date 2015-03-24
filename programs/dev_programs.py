#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" 
Test for hevi_util.program module. 
"""

##############################################################################
## Uses & Setup

import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import unittest # http://docs.python.org/py3k/library/unittest.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)

import hevi_lib.programs

from hevi_lib.programs import Program, manifest



##############################################################################   
## tests

class Test_hevi_util_programs(unittest.TestCase):

  def test_create(self):
    ls = Program("ls","-la")

  def test_run(self):
    true = Program("true")
    true()  
        
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  unittest.main()

