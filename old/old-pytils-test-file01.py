#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: file01.py,v 1.3 2003-08-11 19:48:34 hevi Exp $

"""
"""
__version__ = "$Revision: 1.3 $"

import sys
import os
import unittest
import pytils.file
import pytils.tests.fileops01

class fs_test(unittest.TestCase):
  def __init__(self,methodName):
    unittest.TestCase.__init__(self,methodName)
    
  def setUp(self):
    self.fs = pytils.file.fs()
    
  def tearDown(self):
    pass
    
  def test_mkdir(self):
    self.fs.mkdir("/tmp/test/juu/ei")
    assert(os.path.isdir("/tmp/test/juu/ei"))
    
  def test_mkfifo(self):
    self.fs.mkfifo("/tmp/test/kkk/testfifo")
    ## XXX check

  def test_mklink(self):
    self.fs.mklink("/tmp/test/nnn/jjj","/tmp/test/kkk/testfifo")
    
  def test_mksymlink(self):
    self.fs.mksymlink("/tmp/test/nnn/jjjsym","/tmp/test/kkk")
    ### XXX check

class FsFixed_test(
                   pytils.tests.fileops01.FsProps_test,
                   unittest.TestCase
                   ):
  def __init__(self,methodName):
    unittest.TestCase.__init__(self,methodName)
    pytils.tests.fileops01.FsProps_test.__init__(self,methodName)
    self.filesystem = None
    self.filesystem = pytils.file.FsFixed("/tmp")

  def fs(self):
    return self.filesystem
  

def suite():
  #return unittest.makeSuite(fs_test,'test') # XXX multiple
  return unittest.makeSuite(FsFixed_test,'test')

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

