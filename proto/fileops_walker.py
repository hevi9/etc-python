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
import stat as st


##############################################################################
## Visitors

class AnyVisitor(object):
  """
  """
  
  def visit_object(self,obj):
    """
    @param obj: Any object in stucture.
    @type obj: Any type.  
    """
    pass

class FileVisitor(AnyVisitor):
  """
  """
  
  def visit_dir_enter(self,dir):
    pass
  
  def visit_dir_leave(self,dir):
    pass
  
  def visit_dir(self,dir):
    pass
  
  def visit_file(self,file):
    pass
  
  def visit_error(self,target,exc):
    pass

##############################################################################
## Walker 

class Walker(object):
  
  def __init__(self):
    pass

  def start(self):
    self.run()
    
  def run(self):
    raise RuntimeError("run() not implemented")

##############################################################################
## FileWalker 

class FileWalker(Walker):
  
  def __init__(self,root,visitor,**kwds):
    super(self.__class__,self).__init__()
    self._root = Path(root)
    self._visitor = visitor
    self._follow = kwds.setdefault("follow",False) # follow symlinks
    self._mount = kwds.setdefault("mount",True)   # cross the mountpoint
        
  def run(self):
    follow = self._follow
    mount = self._mount
    root = self._root
    ## root stats
    try:
      if follow:
        root_st = os.stat(root.full_path())
      else:
        root_st = os.lstat(root.full_path())
    except Exception,e:
      raise e;
    ##
    def subwalk(rnpath): # relative node path
      print rnpath
      if len(rnpath) == 0:
        absfile = Path(u"",self._root) # XXX     
      else:
        absfile = Path(os.path.join(*rnpath),self._root)
      log.debug("Walking: " + str(absfile.full_path()))
      ## stat file
      try:
        if follow:
          path_st = os.stat(absfile.full_path())
        else:
          path_st = os.lstat(absfile.full_path())
      except OSError,e:
        print "HERE"
        self._visitor.visit_error(absfile,e)
        return            
      # stop if a symlink and no following
      if st.S_ISLNK(path_st.st_mode) and not follow:
        self._visitor.visit_file(absfile)
        return
      # stop is not same device and no cross mounts
      if path_st.st_dev != root_st.st_dev and not mount:
        if st.S_ISDIR(path_st.st_mode):
          self._visitor.visit_dir(abspath)
        else:
          self._visitor.visit_file(abspath)
        return
      # if directory recurse
      if st.S_ISDIR(path_st.st_mode):
        log.debug("recurse %(absfile)s" % vars())
        absfile = Dir(absfile)
        print absfile.listdir()

        try:
          self._visitor.visit_dir_enter(absfile)
          for name in absfile.listdir():
            rnpath.append(name)
            subwalk(rnpath)
            rnpath.pop()
          self._visitor.visit_leave(absfile)
        except OSError,e:
          print "HERE2"
          self._visitor.visit_error(absfile,e)
          return            
      # is normal file
      else:
        self._visitor.visit_file(absfile)
    ## traverse
    subwalk([])
    
##############################################################################
##   

class test_Files(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    self._tmp_dir = u(tempfile.mkdtemp(u"_walker",u"test_"))
    log.debug(u"tmp_dir: " + self._tmp_dir)
    
  def tearDown(self):
    self.remove_dir(u".")
    unittest.TestCase.tearDown(self)
  
  def remove_dir(self,dir):
    fdir = os.path.join(self.root(),dir)
    for name in os.listdir(fdir):
      fname = os.path.join(self.root(),dir,name)
      if os.path.isdir(fname):
        self.remove_dir(os.path.join(dir,name))
      else:
        log.debug(u"Removing file: " + fname)
        os.remove(fname)
    fdir = os.path.normpath(fdir)
    log.debug(u"Removing dir: " + fdir)
    os.rmdir(fdir)
  
  def root(self):
    return self._tmp_dir
  
  def make_file(self,name):
    fname = u(os.path.join(self.root(),name))
    self.make_dir(os.path.dirname(name))
    log.debug(u"creating file: " + fname)
    fd = open(fname,"wb")
    fd.write(u"ÖÄÅ€ß")
    fd.close()
    return name

  def make_dir(self,name):
    fname = os.path.join(self.root(),name)
    if name == os.sep or name == "":
      return
    if os.path.isdir(fname):
      return
    self.make_dir(os.path.dirname(name))
    log.debug("make_dir: " + fname)
    os.mkdir(u(fname))
    return name

##############################################################################
##   
  
class TestVisitor(FileVisitor):
  def visit_dir_enter(self,dir):
    log.debug("Visit dir enter: " + str(dir))
  
  def visit_dir_leave(self,dir):
    log.debug("Visit dir leave: " + str(dir))
  
  def visit_dir(self,dir):
    log.debug("Visit dir: " + str(dir))
  
  def visit_file(self,file):
    log.debug("Visit file: " + str(file))
  
  def visit_error(self,target,exc):
    log.debug("Visit error: " + str(target) + ": " + str(exc))
  
class test_FileWalker(test_Files):

  def setUp(self):
    super(self.__class__,self).setUp()
    f = self.make_file(u"Ä> <Ö.€")
    f = self.make_file(u"€/Ä.Ö")
      
  def test_proto(self):
    fw = FileWalker(self.root(),TestVisitor())
    log.debug("start ..")
    fw.start()
    
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
