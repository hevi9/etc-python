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
  
  def test_chmod01(self):
    """ chmod """
    #log.debug("some usage")
    filter(upfiles(reallink(sshdir)),user="hevi")
    chmod("somefile","u+rwx,g+r,o+r")

##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
