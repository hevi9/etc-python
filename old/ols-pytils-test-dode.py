#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: dode.py,v 1.1 2004-01-05 11:52:56 hevi Exp $
## UNITTEST

"""
(>>> POINT <<<)
"""
__version__ = "$Revision: 1.1 $"

######################################################################
## depends

import os
import unittest
from pytils.dode import *
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
## test Dode basics

class Dode_test(TestBase):

  def test_support(self):
    """ test support assiciation """
    da = Dode()
    db = Dode()
    da.support(db)
    assert(da in db.depends() and db in da.supports())
    da.unsupport(db)
    assert(da not in db.depends() and db not in da.supports())

  def test_catch_primary_cycle(self):
    """ test catching primary cycle """
    dd = Dode()
    try:
      dd.depend(dd)
    except LoopError,e:
      print "got cycle",e.node
    else:
      assert()

  def text_catch_secondary_cycle(self):
    """ test caching secondary cycle """
    d1 = Dode()
    d2 = Dode()
    d3 = Dode()
    try:
      d1.depend(d2)
      d2.depend(d3)
      d3.depend(d1)
    except LoopError,e:
      print "got cycle",e.node
    else:
      assert()

  def test_diamond(self):
    """ test diamond structure, or basic DAG """
    du = Dode() # up
    dl = Dode() # left
    dr = Dode() # right
    dd = Dode() # down
    ##
    dl.depend(du)
    dr.depend(du)
    dd.depend(dl)
    dd.depend(dr)

  def test_just_call(self):
    """ test just calling the interface (simple) """
    d1 = Dode()
    d2 = Dode()
    d3 = Dode()
    ##
    d1.supports()
    d1.depends()
    try:
      d2.update(d1)
    except:
      pass
    else:
      assert()
    d1.notify()
    ##
    v = Visitor()
    d1.accept(v)
    ##
    d1.subaccept(v)
    ##
    d1.support(d2)
    ##
    d1.unsupport(d2)
    ##
    d1.depend(d2)
    ##
    d1.undepend(d2)

######################################################################
## Targets tests

class Target(Dode):

  def __init__(self,name1):
    Dode.__init__(self)
    self._name = name1

  def name(self,name1 = Void):
    if name1 != Void:
      self._name = name1
    return self._name

class TargetVisitor(Visitor):
  def depthFirst(self):
    return 1
  def visit(self,target1):
    for d in target1.depends():
      print target1.name(),"->",d.name()

class Targets_test(TestBase):

  def test_base(self):
    all = Target("all")
    linkhome = Target("linkhome")
    all.depend(linkhome)
    linkbinpse = Target("linkbinpse")
    linkhome.depend(linkbinpse)
    binpse = Target("binpse")
    linkbinpse.depend(binpse)
    ##
    tv = TargetVisitor()
    all.accept(tv)

  def test_home(self):
    all = Target("all")
    try:
      bindir = os.path.join(os.environ["HOME"],"pse","bin")
      varbindir = os.path.join(os.environ["HOME"],".var","bin")
    except:
      print "no home available, ignoring"
      return
    for filee in os.listdir(bindir):
      frm = Target(os.path.join(bindir,filee))
      to = Target(os.path.join(varbindir,filee))
      to.depend(frm,islink)
      all.depend(to,direct)
    tv = TargetVisitor()
    all.accept(tv)
    

######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(Dode_test,'test'))
  suite.addTest(unittest.makeSuite(Targets_test,'test'))
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




