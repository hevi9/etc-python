#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: fs.py,v 1.2 2005-09-19 13:22:05 hevi Exp $
## MODULE

"""
import pytils.fs as fs

Generic rules:
 * symbolic links are as itself, they are not resolved, unless specidied so

"""
__version__ = "$Revision: 1.2 $"
__todo__ = """
"""



######################################################################
## dependencies

import os
import shutil

######################################################################
## treelistdir

def find(path):
  """
  """
  if not os.path.isdir(path):
    return
  def walk(relpath):
    abspath = os.path.join(path,relpath)
    for name in os.listdir(abspath):
      relpath2 = os.path.join(relpath,name)
      abspath2 = os.path.join(path,relpath2)
      if os.path.isdir(abspath2):
        for item in walk(relpath2):  # recurse into subdir
          yield item
      else:
        yield relpath2
  for item in walk(""):
    yield item

######################################################################
## management

def _copy(src,dst):
  """
  if src is file (including symbolic link to directory)
  if src is dir
  if dst is file
  if dst is dir
  """

def _move(src,dst):
  """
  """

def _remove(src):
  """
  if src is file
  if src is dir
  """


######################################################################
## 

def _compare(src,dst):
  """
  """

######################################################################
## information

def get_link(src):
  """
  """

def is_reg(src):
  """
  """

def is_dir(src):
  """
  """

def is_link(src):
  """
  """

def does_exists(src):
  """
  """

def can_access(src,mode):
  """
  mode:
  r
  w
  x
  """


######################################################################
## 

def _create_dir(src):
  """
  + abspath @str
  """

def _create_file(src):
  """
  + abspath @str
  """

def _create_link(src,dst):
  """
  + abspath @str
  """

def _create_hard_link(src,dst):
  """
  + abspath @str
  """

def _create_fifo(src,mode=0):
  """
  + abspath @str
  """

def _create_node(src,mode=0,device=00):
  """
  + abspath @str
  """

def _create_tmp_file():
  """
  + abspath @str
  """

def _create_tmp_dir():
  """
  + abspath @str
  """

######################################################################
## export

__all__ = (
  "find"
  )

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

