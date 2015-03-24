#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: test_multirun_01.py,v 1.2 2005-01-26 18:40:17 hevi Exp $
## UNITTEST

"""
"""

######################################################################
## dependencies

import unittest
import os
p = os.path

from pyutil.globals import *
import pyutil.multirun as mr
import logging as log

######################################################################
## tests

class TestMultirun(unittest.TestCase):
  """ test just plain importing """

  def test_just(self):
    dir = self.find_test_dir()
    self.fix_perms(dir)
    ###
    #print "DIR",dir
    m1 = mr.Multirun(
      dir=dir,
      prefix="task",
      ignore = ("*~","*.pyc")
    )
    m1.run("clean")
    
  def find_test_dir(self):
    return p.join(p.dirname(__file__),"multirun")

  def fix_perms(self,dir):
    os.system("chmod u+rx %s/*" % dir)

######################################################################
## running

if __name__ == '__main__':
  log.basicConfig()
  log.getLogger().setLevel(log.DEBUG)
  unittest.main()

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
