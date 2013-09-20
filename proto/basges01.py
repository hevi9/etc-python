#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2010 Petri Heinilä, License LGPL 2.1
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

from reportlab.lib.pagesizes import A4


##############################################################################
## Proto

##############################################################################
## Proto usage

class test_Proto(unittest.TestCase):
  
  def test_01(self):
    from reportlab.pdfgen import canvas
    def hello(c):
      c.drawString(100,100,"Hello World")
    c = canvas.Canvas("hello.pdf",pagesize=A4)
    hello(c)
    c.showPage()
    c.save()


##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
