#!/usr/bin/env python
## $Id: termansi.py,v 1.1 2003-07-09 18:34:16 hevi Exp $
## UNITTEST

"""
Test for ansi terminal codes
"""
__version__ = "$Revision: 1.1 $"

######################################################################
## depends

import os
import unittest
import pytils.termansi

######################################################################
## test configuration


######################################################################
## test material


######################################################################
## test base

class TestBase(unittest.TestCase):

  def setUp(self):
    pass
    
  def tearDown(self):
    pass


######################################################################
## test Thing1

class termansi_test(TestBase):

  def test_function(self):
    """ test colors, halftest """
    pytils.termansi.color("test text","black")
    pytils.termansi.color("test text","black","white")
    pytils.termansi.color("test text","black","yellow")
    pytils.termansi.color("test text","yellow","yellow")


######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(termansi_test,'test'))
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




