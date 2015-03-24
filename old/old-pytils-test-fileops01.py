#!/usr/bin/env python
## $Id: fileops01.py,v 1.2 2003-07-08 21:12:00 hevi Exp $
## UNITTEST

"""
"""
__version__ = "$Revision: 1.2 $"

import sys
import os
import unittest
import pytils.spec.file

_debug = 0

class FsProps_test(unittest.TestCase):

  def __init__(self,methodName):
    unittest.TestCase.__init__(self,methodName)

  def fs(self):
    raise NotImplementedError

  def setUp(self):
    pass
    
  def tearDown(self):
    pass

  def test_blockSize(self):
    value = self.fs().blockSize()
    if _debug != 0: print "blockSize",type(value),value
    assert(type(value) == int)

  def test_nameMax(self):
    value = self.fs().nameMax()
    if _debug != 0: print "nameMax",type(value),value
    assert(type(value) == int)

  def test_blocks(self):
    value = self.fs().blocks()
    if _debug != 0: print "blocks",type(value),value
    assert(type(value) == long)

  def test_blocksUsed(self):
    value = self.fs().blocksUsed()
    if _debug != 0: print "blocksUsed",type(value),value
    assert(type(value) == long)

  def test_files(self):
    value = self.fs().files()
    if _debug != 0: print "files",type(value),value
    assert(type(value) == long)

  def test_filesUsed(self):
    value = self.fs().filesUsed()
    if _debug != 0: print "filesUsed",type(value),value
    assert(type(value) == long)

  def test_catchPoint(self):
    value = self.fs().catchPoint()
    if _debug != 0: print "catchPoint",type(value),value
    assert(type(value) == str)

  def test_mountPoint(self):
    value = self.fs().mountPoint()
    if _debug != 0: print "mountPoint",type(value),value
    assert(type(value) == str or value == None)




# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:




