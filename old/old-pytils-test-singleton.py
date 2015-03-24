#!/usr/bin/env python
## $Id: singleton.py,v 1.2 2003-08-13 16:58:59 hevi Exp $
## UNITTEST

"""
"""
__version__ = "$Revision: 1.2 $"

import sys
import os
import unittest
from pytils.common import *

######################################################################
## test material

class _A:
  __metaclass__ = Singleton
  def __init__(self,arg):
    #print "_A(" + str(self) + ").__init__(" + str(arg) + ")"
    self.var = arg
  def __call__(self,arg):
    return arg

class _B(_A):
  def __init__(self,arg):
    _A.__init__(self,arg)
    #print "_B(" + str(self) + ").__init__"

class _C:
  def __init__(self):
    #print "_C(" + str(self) + ").__init__()"
    self.var = 12345

class _D(_C,SingletonBase):
  def __init__(self):
    _C.__init__(self)
    #print "_D(" + str(self) + ").__init__()"

######################################################################
## test singleton

class singleton_test(unittest.TestCase):

  def test_instantiation(self):
    #print "--- same instances for same class:"
    a1 = _A(101)
    a2 = _A() # no meaning for arg
    assert(a1 == a2)
    #print "--- object variables get changed:"
    a1.foo = 100
    a2.foo = 200
    assert(a1.foo == 200)
    #print "--- parameters to the __init__:"
    assert(a2.var == 101)
    #print "--- __call__ works:"
    var = a2(202)
    assert(var == 202)
    #print "--- different instances for A(B) where A is singleton " \
    #      "(and so is B):"
    b1 = _B(10)
    b2 = _B()
    assert(b1 == b2)
    assert(b1 != a1)
    #print "--- C(D) where C is not singleton:"
    d1 = _D()
    d2 = _D()
    assert(d1 == d2)
    assert(d2.var == 12345)

######################################################################
## to testing system

def suite():
  return unittest.makeSuite(singleton_test,'test')

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




