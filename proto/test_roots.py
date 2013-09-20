#!/usr/bin/env python
## -*- coding: utf-8 -*-
## $Id$
## PROTO

"""  """


##############################################################################
## Uses

import sys
import os
import logging
log = logging.getLogger(__name__)
import unittest

##############################################################################
## Roots

##############################################################################
## Proto

class Proto(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
  
  def test_proto(self):
    fs = roots.default()
    fs.make_dir()

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
