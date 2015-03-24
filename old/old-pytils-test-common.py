#!/usr/bin/env python
## $Id: common.py,v 1.3 2003-08-13 16:58:59 hevi Exp $
## UNITTEST

"""
Common functions testing.
"""
__version__ = "$Revision: 1.3 $"

######################################################################
## depends

import os
import unittest
from pytils.common import *

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

class common_test(TestBase):

  def test_relpath(self):
    """ relative path making """
    relpath("/a/b/c","/b/c")

  def test_sort(self):
    """ for in sort """
    l = [1,2,3,4,9,5]
    for i in sort(l):
      pass

  def test_isseq(self):
    """ sequence indentification """
    assert(is_seq(tuple()))
    assert(is_seq(list()))

  def test_gcd(self):
    """ gratest common de.. """
    gcd(100,10)
    gcd(10,100)

  def test_Null(self):
    """ test Null object. """
    # constructing and calling
    Null()
    Null('value')
    Null('value', param='value')
    # attribute handling
    Null.attr1
    Null.attr1.attr2
    Null.method1()
    Null.method1().method2()
    Null.method('value')
    Null.method(param='value')
    Null.method('value', param='value')
    Null.attr1.method1()
    Null.method1().attr1
    Null.attr1 = 'value'
    Null.attr1.attr2 = 'value'
    del Null.attr1
    del Null.attr1.attr2.attr3
    # representation and conversion to a string
    assert repr(Null) == '<Null>'
    assert str(Null) == 'Null'

######################################################################
## property test

class property_test(TestBase):

  def test_doc(self):
    class Test(object):
      prop = Property(None,None,None,"test documentation")
    test = Test()
    assert(Test.prop.__doc__ == "test documentation")

  def test_plain_get(self):
    class Test(object):
      def prop_get(self):
        return 13
      prop = Property(prop_get)
    test = Test()
    assert(test.prop == 13)

  def test_plain_set(self):
    class Test(object):
      def prop_set(self,value):
        assert(value == 13)
      prop = Property(None,prop_set)
    test = Test()
    test.prop = 13

  def test_plain_del(self):
    class Test(object):
      def __init__(self):
        self._prop = 13
      def prop_del(self):
        del self._prop
      prop = Property(None,None,prop_del)
    test = Test()
    test._prop
    del test.prop
    try:
      test._prop
    except AttributeError:
      pass

  def test_inherited_get(self):
    class Base(object):
      def prop_get(self):
        assert(0)
      prop = Property(prop_get)
    class Test(Base):
      def prop_get(self):
        return 13
    test = Test()
    assert(test.prop == 13)

  def test_inherited_set(self):
    class Base(object):
      def prop_set(self,value):
        assert(0)
      prop = Property(None,prop_set)
    class Test(Base):
      def prop_set(self,value):
        assert(value == 13)
    test = Test()
    test.prop = 13

  def test_inherited_del(self):
    class Base(object):
      def prop_del(self):
        assert(0)
      prop = Property(None,None,prop_del)
    class Test(Base):
      def __init__(self):
        self._prop = 13
      def prop_del(self):
        del self._prop
    test = Test()
    test._prop
    del test.prop
    try:
      test._prop
    except AttributeError:
      pass

  def test_3inherited_get(self):
    class Base(object):
      def prop_get(self):
        assert(0)
      prop = Property(prop_get)
    class ITest(Base):
      def prop_get(self):
        return 13
    class Test(ITest):
      pass
    test = Test()
    assert(test.prop == 13)


  def test_3inherited_set(self):
    class Base(object):
      def prop_set(self,value):
        assert(0)
      prop = Property(None,prop_set)
    class ITest(Base):
      def prop_set(self,value):
        assert(value == 13)
    class Test(ITest):
      pass
    test = Test()
    test.prop = 13


  def test_3inherited_del(self):
    class Base(object):
      def prop_del(self):
        assert(0)
      prop = Property(None,None,prop_del)
    class ITest(Base):
      def __init__(self):
        self._prop = 13
      def prop_del(self):
        del self._prop
    class Test(ITest):
      pass
    test = Test()
    test._prop
    del test.prop
    try:
      test._prop
    except AttributeError:
      pass

######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(common_test,'test'))
  suite.addTest(unittest.makeSuite(property_test,'test'))
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




