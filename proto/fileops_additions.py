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
import hevi_util.fileops

##############################################################################
## Proto

class FileSystem(hevi_util.fileops.FileOps):
    
  def copy_task(self,src,dst,**kwds):
    pass
  
  def merge_task(self,src,dst,**kwds): # needed ?
    pass
  

def default():
  return FileSystem()


##############################################################################
## Proto

class Proto(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
  
  def test_proto(self):
    pass

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
