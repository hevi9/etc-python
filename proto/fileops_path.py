#!/usr/bin/env python
## -*- coding: utf-8 -*-
## $Id$
## PROTO

"""  
Path is a proxy to files ?

Related:
  * http://www.python.org/dev/peps/pep-0355/
  * http://mail.python.org/pipermail/python-dev/2005-June/054439.html
"""


##############################################################################
## Uses
## test

import sys
import os
import logging
log = logging.getLogger(__name__)

##############################################################################
## Utils

class Void(object): pass

##############################################################################
## Path

class Path(object):
  """ Path specification to some resource. The resoource might exists
  or not. Path here is just information no file system (or access system)
  assumptions are not done yet.
  """
  
  def __init__(self,spec):
    """
    @param spec: A path specification. Could be relative or absolute.
    @type spec: str | unicode | Path
    """
  
  ############################################################      
  ## naming & representation
    
  def spec(self,value=Void):
    """
    @rtype: unicode
    """
    if not value is Void:
      self._spec = value
    return self._spec

  def root(self,value=Void):
    """
    @rtype: unicode
    """
    if not value is Void:
      self._root = value
    return self._root

  def full_path(self):
    """
    @rtype: unicode    
    """
    if not self._root is None:
      return os.path.join(self._root,self._spec)
    else:
      return self._spec 

  def name(self): # as basename
    """
    @rtype: unicode    
    """
    return os.path.basename(self._spec)

  ############################################################      
  ## existense

  def exists(self):
    """  """
    if os.path.exists(self._spec): # spec directly exists
      return True
    if os.path.exists(self.full_path()): # is root & spec exists
      return True
    return False

  def link_exists(self):
    """  """
    if os.path.lexists(self._spec): # spec directly exists
      return True
    if os.path.lexists(self.full_path()): # is root & spec exists
      return True
    return False

  def is_abs(self):
    """  """
    return os.path.isabs(self._spec)

  def is_file(self):
    """  """
    return os.path.isfile(self._spec)
    
  def is_dir(self):
    """  """
    return os.path.isdir(self._spec)

  def is_link(self):
    """  """
    return os.path.islink(self._spec)

  def is_mount(self):
    """  """
    return os.path.ismount(self._spec)

  ## creation

  def join(self,*other):
    """ """
    return os.path.join(self.spec(),*other)

  ## representation

  def __str__(self):
    """
    """
    return self._spec
  
  def __repr__(self):
    return '%s(%r)' % (self.__class__.__name__, str(self))  
  
  ## creations

  def file(self):
    """ Return a File object based on this path.
    @return: 
    @rtype: File
    """
    if type(self) is File:
      return self
    else:
      return File(self)

  def dir(self):
    """ Return a Directory object based on this path.
    @return: 
    @rtype: Dir
    """
    if type(self) is Dir:
      return self
    else:
      return File(self)
  

##############################################################################
## File  

##############################################################################
## Dir

class Dir(Path):
  """ """
  def __init__(self,*args):
    super(self.__class__,self).__init__(*args)
    
  def listdir(self):
    """ Return file names in this directory.
    """
    return os.listdir(self.full_path())
    
  def listdir_paths(self):
    """
    """
    pass
      
##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
