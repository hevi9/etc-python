#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: test_module_01.py,v 1.1 2005-01-26 15:48:05 hevi Exp $
## UNITTEST

"""
"""

######################################################################
## dependencies

import unittest
import os
j = os.path.join
p = os.path
import logging as log
import sys
import pyutil.module as mdl

######################################################################
## config

root = "/tmp/pyutil_test"

######################################################################
## tests

def sys_path_search(filename):
  for dir in sys.path:
    file = j(dir,filename)
    if p.exists(file):
      return file
  return None

class TestModule(unittest.TestCase):
  
  def test_some(self):
    mp = sys_path_search("fpformat.py")
    if not mp: return
    m = mdl.import_named_file(mp)
  
######################################################################
## running

if __name__ == '__main__':
  unittest.main()

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
