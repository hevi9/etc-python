#!/usr/bin/env python
## $Id: log01.py,v 1.3 2003-08-13 16:58:59 hevi Exp $

"""
"""
__version__ = "$Revision: 1.3 $"

import sys
import os
import unittest
import pytils.log
from pytils.log import log

def suite():

  class log_test(unittest.TestCase,pytils.spec.log.Messages):
    def __init__(self,methodName):
      unittest.TestCase.__init__(self,methodName)
      pytils.log.props.debug = 1
      self.got = None
    
    def setUp(self):
      log.addWriter(self)
    
    def tearDown(self):
      log.remove_writer(self)
    
    def test_info(self):
      log.info("info test")
      assert(self.got == "info test")
    
    def test_debug(self):
      log.debug("debug test")
      assert(self.got == "debug test")

    def test_error(self):
      log.error("error test")
      assert(self.got == "error test")
    
    def test_system(self):
      log.system("system test")
      assert(self.got == "system test")

    def info(self,*msg):
      self.got = ",".join(msg)
      
    def debug(self,*msg):
      self.got = ",".join(msg)
      
    def error(self,*msg):
      self.got = ",".join(msg)
      
    def system(self,*msg):
      self.got = ",".join(msg)

  return unittest.makeSuite(log_test,'test')


def check():
  runner = unittest.TextTestRunner(verbosity=1)
  result = runner.run(suite())
  return not result.wasSuccessful()

if __name__ == '__main__':
  check()


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

