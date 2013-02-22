#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
"""
File browser.
"""

##############################################################################
## Uses & module setup

import os # http://docs.python.org/py3k/library/os.html

__all__ = list()

##############################################################################
## functions

def make_rplist(rp):
  """ Convert str path into list path. """
  r = list()
  p = rp
  t = os.path.split(p)
  r.append(t[1])
  while t[1] is not '':
    p = t[0]
    t = os.path.split(p)
    r.append(t[1])
  r.reverse()
  return r

__all__.append(make_rplist.__name__)

