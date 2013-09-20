#!/usr/bin/env python
## $Id: file.py,v 1.3 2003-07-29 21:30:41 hevi Exp $
## SPECIFICATION

""" File operations specification.
"""

class __nothing: pass

######################################################################
## depends

from pytils.spec.exc import *


######################################################################
## file operations interface

class _UnderConsideration(type):
  """
  access
  chdir
  chown
  fchown
  fchdir
  fsync
  getcwd
  lchown
  link
  lockf
  rmdir
  symlink
  unlink
  chgrp

  - conforms object interface
  
  """

  def equal(self,file1,file2):
    """ equal(file1@str,file2@str)@boolean, raises None:
    """
    raise NotImpelmentedError

######################################################################
## file management operations interface

class Operations(object):
  """
  """

  ## creation

  def mkdir(self,path,mode):
    """
    """
    raise NotImplementedError

  def mkfifo(self,path,mode):
    """
    """
    raise NotImplementedError

  def mklink(self,path,target):
    """
    linking directories
    """
    raise NotImplementedError

  def mksymlink(self,path,target):
    """
    """
    raise NotImplementedError

  def create_file_notify(self,path): ## mkfile_notify
    """
    """
    raise NotImplementedError

  ## removal

  def unlink(self,path):
    """
    """
    raise NotImplementedError

  ## relocation

  def move(self,path,target):
    """
    """
    raise NotImplementedError

  ## duplicating

  def copy(self,path,target):
    """
    """
    raise NotImplementedError

  ## properties

  def chmod(self,path,mode):
    """
    """
    raise NotImplementedError

  def chown(self,path,uid,gid):
    """
    """
    raise NotImplementedError

  ## information

  def listdir(self,path):
    """
    """
    raise NotImplementedError

  def stat(self,path):
    """
    """
    raise NotImplementedError

  def lstat(self,path): # ?
    """
    """
    raise NotImplementedError

  def readlink(self,path):
    """
    """
    raise NotImplementedError

######################################################################
## FsProps

class FsProps(object):
  """ File system properties.
  """ 
    
  def blockSize(self):
    """
    File system block size in bytes.
    = @int
    = safe
    = readonly
    = property, pass through
    """
    raise NotImplementedError
  
  def nameMax(self):
    """
    Maximun lenght of the name in file system.
    = @int
    = safe
    = readonly
    = property, pass through
    """
    raise NotImplementedError
  
  def blocks(self):
    """
    Total number of the blocks in the file system.
    = @long
    = safe
    = readonly
    = property, pass through
    """
    raise NotImplementedError
  
  def blocksUsed(self):
    """
    Block used in the file system.
    = @long
    = safe
    = readonly
    = property, pass through
    """
    raise NotImplementedError
  
  def files(self):
    """
    Total number of available files in the file system.
    = @long
    = safe
    = readonly
    = property, pass through
    """
    raise NotImplementedError
  
  def filesUsed(self):
    """
    Number of the file used in the file system.
    = @long
    = safe
    = readonly
    = property, pass through
    """
    raise NotImplementedError

  def catchPoint(self):
    """
    Path wherefrom the file system if cathed on instantiation.
    = @str
    = safe
    = readonly
    = property, pass through
    ? none
    """
    raise NotImplementedError

  def mountPoint(self):
    """
    Path, where file system is mounted.
    = @str|None is a str or None if mount point information is not available.
    = safe
    = readonly
    = property, pass through
    ? none
    """
    raise NotImplementedError

######################################################################
##
## is
## equal
## name
## object, objectN
## id
## content
## exists
## name
## copy
## destroy
## move
## node
## create
## dir
## content
## file
## link
## target
## owner
## group
## access
## type
## user
## current

class ObjectOps(object):
  def is_equal_name(self,object1_id,object2_id):
    """
    """
    raise NotImplementedError

  def is_equal_content(self,object1_id,object2_id):
    """
    """
    raise NotImplementedError

  def is_exists(self,object_id):
    """
    """
    raise NotImplementedError

  def name(self,object_id):
    """
    """
    raise NotImplementedError

  def copy(self,object1_id,object2_id):
    """
    """
    raise NotImplementedError

  def destroy(self,object_id):
    """
    """
    raise NotImplementedError


class NodeOps(ObjectOps):
  def move(self,node1_id,node2_id):
    """
    """
    raise NotImplementedError

class DirOps(object):
  def create_dir(self,dir_id):
    """
    """
    raise NotImplementedError

  def is_dir(self,node_id):
    """
    """
    raise NotImplementedError

  def content(self):
    """
    """
    raise NotImplementedError

class FileOps(object):

  def create_file(self,file_id):
    """
    """
    raise NotImplementedError

  def is_file(self,node_id):
    """
    """
    raise NotImplementedError

class LinkOps(object):

  def create_link(self,link_id):
    """
    """
    raise NotImplementedError

  def is_link(self,node_id):
    """
    """
    raise NotImplementedError

  def target(self):
    """
    """
    raise NotImplementedError

# access types
class access_type(object): pass
class access_read(access_type): pass
class access_write(access_type): pass
class access_execute(access_type): pass

# user types
class user_type(object): pass # type ?
class user_owner(user_type): pass
class user_group(user_type): pass
class user_all(user_type): pass
class user_current(user_type): pass

class SecurityOps(object):

  def set_owner(self,node_id,owner_id):
    """
    """
    raise NotImplementedError

  def get_owner(self,node_id):
    """
    """
    raise NotImplementedError

  def set_group(self,node_id,group_id):
    """
    """
    raise NotImplementedError

  def get_group(self,group_id):
    """
    """
    raise NotImplementedError

  def has_access(self,node_id,access_type,user_type = user_current):
    """
    """
    raise NotImplementedError

  def set_access(self,node_is,access_type,user_type = user_current):
    """
    """
    raise NotImplementedError


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
