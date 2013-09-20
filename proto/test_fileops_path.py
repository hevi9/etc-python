#!/usr/bin/env python
## -*- coding: utf-8 -*-
## $Id$
## PROTO

"""  """


##############################################################################
## Uses
## test

import sys
import os
import logging
log = logging.getLogger(__name__)
import unittest
import tempfile
u = unicode
from proto.fileops_path import *

##############################################################################
## Utils    
    
def dump_path(p1):
  print "Path: '"+str(p1)+"'"
  # naming
  print " spec(): '"+p1.spec()+"'"
  print " root(): '"+str(p1.root())+"'"
  print " full_path(): '"+str(p1.full_path())+"'"
  print " name(): '"+p1.name()+"'"
    
    
##############################################################################
## 

class test_Path(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
  
  def test_creation_1(self):
    self.assertRaises(AssertionError,
                      Path,"/absolute","relative")
  
  def test_creation_2(self):
    p1 = Path(u"relative")
    #self._all_ops(p1)

    p1 = Path(u"/absolute")
    #self._all_ops(p1)

    p1 = Path(u"relative.€",u"/absolute")
    #self._all_ops(p1)

    p1 = Path(u"/tmp")
    #self._all_ops(p1)

    p1 = Path(u"/")
    #self._all_ops(p1)

  def test_creation_3(self):
    p1 = Path("relative")
    #self._all_ops(p1)

    p1 = Path("/absolute")
    #self._all_ops(p1)

    p1 = Path("relative.€",u"/absolute")
    #self._all_ops(p1)

    p1 = Path("/tmp")
    #self._all_ops(p1)

    p1 = Path("/")
    #self._all_ops(p1)

  def test_creation_4(self):
    p1 = Path(Path("relative"))
    #self._all_ops(p1)

    p1 = Path(Path("/absolute"))
    #self._all_ops(p1)

    p1 = Path(Path(u"relative.€"),Path("/absolute"))
    #self._all_ops(p1)

    p1 = Path(Path("/tmp"))
    #self._all_ops(p1)

    p1 = Path(Path("/"))
    #self._all_ops(p1)
    
  def test_creation_5(self):
    """ spec = unicode & root = Path """
    ##
    pr = Path("relative/root")
    pt = Path(u"name",pr)
    self.failUnlessEqual(pt.root(),pr.spec(),"root settings")
    #dump_path(pt)
    ##
    pr = Path("relative/root")
    pt = Path(u"",pr)
    self.failUnlessEqual(pt.root(),pr.spec(),"root settings")
    #dump_path(pt)

  def _all_ops(self,p1):
    print "str",p1,"spec",p1.spec(),"root",p1.root()
    print "  is_abs",p1.is_abs(),"full_path",p1.full_path()
    print "  exists",p1.exists(),"link_exists",p1.link_exists(),
    print "  name",p1.name()
      
##############################################################################
## Test Dir 

class test_Dir(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
            
  def test_creation_1(self):
    p1 = Path("spec/path","root/path")
    d1 = Dir(p1)
    dump_path(d1)
    ##
    p1 = Path("","root/path")
    d1 = Dir(p1) # XXX VS Dir(p1,"root") -> conflicting semantics
    dump_path(d1)
    ##
    p1 = Path("","root/path")
    d1 = Dir(p1,"/some/root")
    dump_path(d1)

    
  def test_listdir(self):
    pass
    
  def test_listdir_paths(self):
    pass
      
      
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
