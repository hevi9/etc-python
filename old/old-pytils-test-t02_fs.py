#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: t02_fs.py,v 1.1 2004-04-19 16:02:58 hevi Exp $
## UNITTEST

"""
(>>> POINT <<<)
"""
__version__ = "$Revision: 1.1 $"

######################################################################
## depends

import sys
sys.path.append("..") # XXX

import os
import unittest
import music.fs as fs
import tempfile
import shutil as sh

######################################################################
## test configuration


######################################################################
## test material


######################################################################
## test base

class TestBase(unittest.TestCase):

  def setUp(self):
    self.root = tempfile.mkdtemp()
    print "test root",self.root
    ## populate
    file1 = os.path.join(self.root,"file1")
    f = file(file1,"w")
    f.close()

    
  def tearDown(self):
    sh.rmtree(self.root)
    print "test root",self.root,"removed"
    


######################################################################
## test Thing1

class Fs_test(TestBase):

  def test_treelistdir(self):
    """ test recursive tree listing """
    for path in fs.treelistdir("."):
      print path
    assert(0)


######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(Fs_test,'test'))
  return suite

def check():
  runner = unittest.TextTestRunner(verbosity=1)
  result = runner.run(suite())
  return not result.wasSuccessful()

if __name__ == '__main__':
  check()


######################################################################
# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:




