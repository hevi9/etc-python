#!/usr/bin/env python
## $Id: file.py,v 1.19 2003-08-13 11:46:44 hevi Exp $

"""
File management operations interface and basic implementation.


Management interface vs direct object inteface
----------------------------------------------

 * Manager object
 * stateless

manager.equal(object1,object2) -> boolean

object1.equal(object2) -> boolean

"""
__version__ = "$Revision: 1.19 $"
__todo__ = """
5 reorganize
5 define complete interfaces
"""

from __future__ import generators

if __name__ == '__main__':
  import pytils.file
  import sys
  sys.exit(pytils.file.check()) # or check()

_debug = 0

######################################################################
## depends
  
import sys
import os
import errno
import stat
from pytils.log import log
from pytils.spec.exc import *
from pytils.spec.file import *

######################################################################
## object management interface

class object_mgmt(object):

  def mkobject_notify(self,object):
    """
    """
    raise NotImplementedError

  def copy(self,object,target):
    """
    synonyms:
    - duplicate()
    - clone()
    issues:
    - deep copy vs swallow copy
    """
    raise NotImplementedError

######################################################################
## file system
## dryrun !!!!!!!

class FsBasic(Operations):
  """ Convient file system operations.
  Target situation based operations. This means that if the situation
  is already in wanted state, no operation none or error is raised.
  For exmaple on unlink() if given file does not exists it does nothing.
  """

  def __init__(self):
    pass

  ## creation

  def mkdir(self,file,mode=0777):
    if file == "":
      return file
    if os.path.isdir(file):
      if not os.access(file,os.X_OK):
        raise IOError,file + " user has no executece access"
      return file
    if os.path.exists(file):
      raise IOError,file + " exists and is not a directory"
    self.mkdir(os.path.split(file)[0],mode)
    log.system("directory",file,str(oct(mode)),"create")
    os.mkdir(file,mode)
    return file    

  def mkfifo(self,file,mode = 0666):
    if os.path.exists(file) and stat.S_ISFIFO(os.stat(file).st_mode):
      return file
    self.mkdir(os.path.dirname(file))
    log.system("fifo",file,str(oct(mode)),"create")
    os.mkfifo(file,mode)
    return file

  def mklink(self,file,target):
    """
    - cannot link to directory
    """
    if (os.path.exists(file) and
        os.path.exists(target) and
        os.stat(file).st_ino == os.stat(target).st_ino):
      return file
    self.mkdir(os.path.dirname(file))
    log.system("link",file,"->",target)
    os.link(target,file)
    return file
    

  def mksymlink(self,file,target):
    if (os.path.islink(file) and
        os.readlink(file) == target):
      return file
    self.mkdir(os.path.dirname(file))
    log.system("symlink",file,"->",target)
    os.symlink(target,file)
    return file

  def create_file_notify(self,file):
    if not os.path.exists(file):
      self.mkdir(os.path.dirname(file))
      log.info("create file",file)

  ## removal

  def unlink(self,file):
    if not os.path.exits(file):
      return file
    log.system("unlink",file)
    os.unlink(file)

  ## relocation

  def move(self,file,target):
    raise NotImplementedError

  def copy(self,file,target):
    raise NotImplementedError
    
  ## properties

  def chmod(self,file,mode):
    st = os.stat(file)
    if stat.S_IMODE(st.st_mode) != mode:
      log.info("mode",file,oct(mode))
      os.chmod(file,mode)

  def chown(self,file,uid,gid):
    raise NotImplementedError

  ## information

  def listdir(self,file):
    return os.listdir(file)

  def stat(self,file):
    raise NotImplementedError

  def lstat(self,file): # ?
    raise NotImplementedError

  def readlink(self,file):
    raise NotImplementedError


FS = FsBasic
fs = FsBasic
  

"""
  def _mount(self):
    return
  def unmount(self):
    return
"""

######################################################################
## recursive directory listing
## - based on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/105873

#def listdir(dir):
#  try:
#    for f in os.listdir(dir):
#      fullpath = os.path.join(dir,f)
#      if os.path.isdir(fullpath) and not os.path.islink(fullpath):
#        for x in listdir(fullpath):  # recurse into subdir
#          yield x
#      else:
#        yield fullpath
# some error here




######################################################################
## 

class file_props(object): # interface
  pass

class file(object):
  def getatime(self):
    return os.path.getatime(str(self))
  def getmtime(self):
    return os.path.getmtime(str(self))
  def getsize(self):
    return os.path.getsize(str(self))
  def isregular(self):
    return os.path.isfile(str(self))
  def isdir(self):
    return os.path.isdir(str(self))
  def islink(self): # in path ?
    return os.path.islink(str(self))
  def ismount(self):
    return os.path.ismount(str(self))
  def XXX_isCharDevice(self):
    return None
  def XXX_isBlockDevice(self):
    return None
  def XXX_isFifo(self):
    return None
  def XXX_isSocket(self):
    return None
  def XXX_location(self):
    # return (device,type,inode,links)
    return None
  def XXX_getUser(self):
    return None
  def XXX_setUser(self):
    return None
  def XXX_getGroup(self):
    return None
  def XXX_setGroup(self):
    return None
  def XXX_fs(self):
    """ fs() @fileSystem:
    Returns the filesystem, where file resides.
    """
  def mkdir(cls,apath,mode=0777):
    """ file.mkdir(apath@path, mode@int = 0777) @ file, raise IOError:
    """
    if type(apath) == str:
      apath = path(apath)
    if type(apath) != path:
      raise TypeError,"apath is not type path"
    #print apath,len(apath)
    for i in range(1,len(apath)+1):
      p = file(apath[:i])
      #print p
      if p.isdir():
        if not os.access(p,os.X_OK):
          raise IOError,p + " user has no executece access"
        continue
      if p.exists():
        raise IOError,p + " exists and is not a directory"
      log.system(p,"directory create")
      os.mkdir(p,mode)
    return file(apath)
  mkdir = classmethod(mkdir)

  def mksymlink(cls,apath,target):
    """ file.symlink(linkfile@str,target@str) @str,raises IOError:
    """
    try:
      os.symlink(target,apath)
    except OSError,(errnro,errstr):
      if errnro == errno.EEXIST:
        if os.path.islink(apath) and os.readlink(apath) != target:
          raise ExistsError
      else:
        raise OSError(errnro,errstr)
    else:
      log.system("symlinking:",apath,target)
  mksymlink = classmethod(mksymlink)

######################################################################
##


class FsFixed(FS,FsProps):
  """
  """

  def __init__(self,path):
    """
    ? ValueError path is not absolute
    """
    if not os.path.isabs(path):
      raise ValueError
    self.path = path
    self.stats = None
    self.update()

  def blockSize(self):
    return self.stats.f_frsize
  
  def nameMax(self):
    return self.stats.f_namemax
  
  def blocks(self):
    return self.stats.f_blocks
  
  def blocksUsed(self):
    return self.stats.f_blocks - self.stats.f_bfree
  
  def files(self):
    return self.stats.f_files
  
  def filesUsed(self):
    return self.stats.f_files - self.stats.f_ffree

  def catchPoint(self):
    return self.path

  def mountPoint(self):
    parts = self.path.split(os.sep)
    if _debug: print self.path
    if _debug: print parts,len(parts)
    while len(parts):
      path = os.sep.join(parts)
      if len(path) == 0 : path = '/'
      if os.path.ismount(path):
        return path
      parts.pop()
    return None
  
  def update(self):
    """ Update information.
    """
    if not os.path.exists(self.path):
      raise NotExistsError(self.path + " does not exists")
    self.stats = os.statvfs(self.path)
    

######################################################################


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

