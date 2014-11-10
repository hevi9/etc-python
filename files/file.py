#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1
""" 
File data access
================ 

"""

##############################################################################
## Uses & Setup
import sys # http://docs.python.org/py3k/library/sys.html
import os # http://docs.python.org/py3k/library/os.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
import stat # http://docs.python.org/py3k/library/stat.html
import inspect # http://docs.python.org/py3k/library/inspect.html
import mimetypes # http://docs.python.org/py3k/library/mimetypes.html
from hevi_proto.util import PropsDict
## python-magic don't work
#import magic # https://github.com/ahupp/python-magic

__all__ = list()

##############################################################################
## File

class File:
  
  def __init__(self,path):
    assert os.path.isabs(path)
    self._path = path # absolute path
    self._st = os.lstat(path)
    ##
    self.props = PropsDict(self)
    
  ## file operations
  
  def subfile(self,name:str):
    return File(os.path.join(self.path,name))

  def listdir(self):
    return os.listdir(self.path)
    
  ## file information by property

  @property #1
  def path(self): return self._path

  @property #2
  def st(self): return self._st

  @property #3
  def isdir(self): return stat.S_ISDIR(self.st.st_mode) 

  @property #4
  def ischr(self): return stat.S_ISCHR(self.st.st_mode) 

  @property #5
  def isblk(self): return stat.S_ISBLK(self.st.st_mode) 

  @property #6
  def isreg(self): return stat.S_ISREG(self.st.st_mode) 

  @property #7
  def isfifo(self): return stat.S_ISFIFO(self.st.st_mode) 

  @property #8
  def islnk(self): return stat.S_ISLNK(self.st.st_mode) 

  @property #9
  def issock(self): return stat.S_ISSOCK(self.st.st_mode) 

  @property #10
  def mode(self): return self._st.st_mode 

  @property #11
  def ino(self): return self._st.st_ino 

  @property #12
  def dev(self): return self._st.st_dev 

  @property #13
  def nlink(self): return self._st.st_nlink 

  @property #14
  def uid(self): return self._st.st_uid 

  @property #15
  def gid(self): return self._st.st_gid 

  @property #16
  def size(self): return self._st.st_size 

  @property #17
  def atime(self): return self._st.st_atime 

  @property #18
  def ctime(self): return self._st.st_ctime 

  @property #19
  def mtime(self): return self._st.st_mtime 

  @property #20
  def blocks(self): return self._st.st_blocks 

  @property #21
  def blksize(self): return self._st.st_blksize 

  @property #22
  def rdev(self): return self._st.st_rdev 

  @property #23
  def name(self): return os.path.basename(self._path)

  @property #24
  def chtype(self):
    """System file type as character. """ 
    if self.isdir:
      return "D"
    elif self.ischr:
      return "c"
    elif self.isblk:
      return "b"
    elif self.isfifo:
      return "f"
    elif self.isreg:
      return "F"
    elif self.islnk:
      return "L"
    elif self.issock:
      return "S"
    else:
      return "E"
  
  ## don't work
  #@property #23
  #def mimetype(self): return magic.from_file(self._path) # XXX wrong type ex

__all__.append("File")

##############################################################################
## Dev Test

if __name__ == "__main__":
  a = File("/")
  print("File {0}".format(a.path))
  for key in sorted(a.props):
    print("  {0} = {1} as {2}".format(key,a.props[key],type(a.props[key])))




