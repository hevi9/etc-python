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

##############################################################################
## Proto

#import os

## unknow situation, try & crash
# assert os.path.supports_unicode_filenames


class Void(object): pass

class Path(object):
  """ Path specification to some file. File might exists
  or not.
  """
  
  def __init__(self,spec,root=None):
    """
    @param spec:
    @type spec: str | unicode | Path
    @param root:
    @type root: str | unicode | Path | None
    """
    # spec
    if type(spec) is Path:
      self._spec = spec.spec()
    elif type(spec) is str:
      log.debug("converting '" + spec + "' to unicode")
      self._spec = unicode(spec) # forced unicode usage
    elif type(spec) is unicode:
      self._spec = spec
    else:
      raise TypeError(u"Invalid type " + u(type(spec)) + u" for spec")
    # root
    if root is None:
      self._root = root
    elif type(root) is Path:
      self._root = root.root()
    elif type(root) is str:
      log.debug("converting '" + root + "' to unicode")
      self._root = unicode(root) # forced unicode usage
    elif type(root) is unicode:
      self._root = root
    else:
      raise TypeError(u"Invalid type " + u(type(root)) + u" for root")    
    # cannot have absolute spec and root definition at same time
    assert not (os.path.isabs(self._spec) and not self._root is None), "cannot have abs spec and root"
        
  ## naming
    
  def spec(self,value=Void):
    """
    """
    if not value is Void:
      self._spec = value
    return self._spec

  def root(self,value=Void):
    """
    """
    if not value is Void:
      self._root = value
    return self._root

  def full_path(self):
    """
    """
    if not self._root is None:
      return os.path.join(self._root,self._spec)
    else:
      return self._spec 

  def name(self): # as basename
    return os.path.basename(self._spec)

  ## existense

  def exists(self):
    """ TODO: DOC """
    if os.path.exists(self._spec): # spec directly exists
      return True
    if os.path.exists(self.full_path()): # is root & spec exists
      return True
    return False

  def link_exists(self):
    """ TODO: DOC """
    if os.path.lexists(self._spec): # spec directly exists
      return True
    if os.path.lexists(self.full_path()): # is root & spec exists
      return True
    return False

  def is_abs(self):
    """ TODO: DOC """
    return os.path.isabs(self._spec)

  def is_file(self):
    """ TODO: DOC, root """
    return os.path.isfile(self._spec)
    
  def is_dir(self):
    """ TODO: DOC, root """
    return os.path.isdir(self._spec)

  def is_link(self):
    """ TODO: DOC, root """
    return os.path.islink(self._spec)

  def is_mount(self):
    """ TODO: DOC, root """
    return os.path.ismount(self._spec)

  ## creation

  def join(self,other):
    pass

  ## representation

  def __str__(self):
    """
    """
    return self._spec

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
  
  def visit_file(self,file):
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
  
  def __init__(self,root):
    super(self.__class__,self).__init__()
    self._root = Path(root)
        
  def run(self):
    pass
    
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
    self._all_ops(p1)

    p1 = Path(u"/absolute")
    self._all_ops(p1)

    p1 = Path(u"relative.€",u"/absolute")
    self._all_ops(p1)

    p1 = Path(u"/tmp")
    self._all_ops(p1)

    p1 = Path(u"/")
    self._all_ops(p1)

  def test_creation_3(self):
    p1 = Path("relative")
    self._all_ops(p1)

    p1 = Path("/absolute")
    self._all_ops(p1)

    p1 = Path("relative.€",u"/absolute")
    self._all_ops(p1)

    p1 = Path("/tmp")
    self._all_ops(p1)

    p1 = Path("/")
    self._all_ops(p1)

  def test_creation_4(self):
    p1 = Path(Path("relative"))
    self._all_ops(p1)

    p1 = Path(Path("/absolute"))
    self._all_ops(p1)

    p1 = Path(Path(u"relative.€"),Path("/absolute"))
    self._all_ops(p1)

    p1 = Path(Path("/tmp"))
    self._all_ops(p1)

    p1 = Path(Path("/"))
    self._all_ops(p1)


  def _all_ops(self,p1):
    return
    print "str",p1,"spec",p1.spec(),"root",p1.root()
    print "  is_abs",p1.is_abs(),"full_path",p1.full_path()
    print "  exists",p1.exists(),"link_exists",p1.link_exists(),
    print "  name",p1.name()
  


class test_unicode(unittest.TestCase):

  def setUp(self):
    unittest.TestCase.setUp(self)
    
  def tearDown(self):
    unittest.TestCase.tearDown(self)
  
  def test_file(self):
    return
    self._tmp_dir = tempfile.mkdtemp("unicode","test")
    log.debug("tmp_dir: " + self._tmp_dir)
    #
    name = u"Ä> <Ö.€"
    fname = os.path.join(self._tmp_dir,name)
    log.debug(u"creating file: " + fname)
    fd = open(fname,"wb")
    fd.write(u"ÖÄÅ€ß")
    fd.close()
  
  def test_uc1(self):
    return
    print "FS Properties:"
    print "  Default encoding:",sys.getdefaultencoding()
    print "  Filesystem encoding:",sys.getfilesystemencoding()
    print "  Current directory char: ",os.curdir
    print "  Parent dircetiory char: ",os.pardir
    print "  Path separator: ",os.sep
    print "  Path alternative separator: ",os.altsep
    print "  Filename extersion separtor: ",os.extsep
    print "  Search path separator: ",os.pathsep
    print "  Supports unicode filenames: ",os.path.supports_unicode_filenames

  def test_confstr(self):
    return
    for name in os.confstr_names:
      print name, " = ",os.confstr(name)

  def test_sysconf(self):
    return
    for name in os.sysconf_names:
      print name, " = ",os.sysconf(name)

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
  
class test_FileWalker(test_Files):

  def setUp(self):
    super(self.__class__,self).setUp()
    f = self.make_file(u"Ä> <Ö.€")
    f = self.make_file(u"€/Ä.Ö")
      
  def test_proto(self):
    fw = FileWalker(self.root())
    fw.start()
    
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
