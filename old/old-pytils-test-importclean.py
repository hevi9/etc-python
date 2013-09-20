#!/usr/bin/env python
## $Id: importclean.py,v 1.3 2003-08-11 19:48:34 hevi Exp $
## UNITTEST

"""
Test for ansi terminal codes
"""
__version__ = "$Revision: 1.3 $"

######################################################################
## depends

import os
import sys
import unittest
import pytils.module

######################################################################
## test configuration


######################################################################
## test material


######################################################################
## test base and test utils

class TestBase(unittest.TestCase):

  def setUp(self):
    pass
    
  def tearDown(self):
    pass


######################################################################
## test Thing1

class importclean_test(TestBase):

  def test_clean_import(self):
    """ test clean import for *all* python modules """
    importer = pytils.module.Importer()
    root,path,type = importer.find_module("pytils")
    ##
    files = importer.find_sub_moduleFiles(root,"pytils")
    for file in files:
      qname = importer.path2qname(os.path.join("pytils",file))
      __import__(qname)
      # this hides the origin
      #try:
      #  __import__(qname)
      #except ImportError,e:
      #  raise ImportError(file + ", " + qname + ", " + str(e))
    

######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(importclean_test,'test'))
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




