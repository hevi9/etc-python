#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id$
## MODULE

assert False,"Not for use"

"""
Convience interface to system scripting.


dir/dir/name.ext
/dir/dir/name.ext
         ^      ^ ? => part

/dir/dir/apackage-0.1.2.3.tar.gz
^ dir   ^        name          ^
        ^     base       ^ ext ^



join() is opposite operation for nodes
- or should join() be path() ie new path constrction



Migration:
 * part => node

"""
__version__ = "$Revision$"
__docformat__ = "plaintext"

"""
Names:
 * cwd - current working directory, context: process
"""

######################################################################
## dependencies

import os
import shutil
import sys
import fnmatch
import glob
import shutil
import codecs
import mimetypes
import errno
from pyutil.common import Void,is_seq,Null

cfg_dryrun = False

CD = os.curdir  # .
UP = os.pardir  # ..
DS = os.sep     # /
ES = os.extsep  # .
PS = os.pathsep # :
NL = os.linesep #

######################################################################
## UI

class Ui(object):
  
  def remove(self,dsts,msg):
    print "REMOVE",dsts,msg

  def modify(self,dsts,msg):
    print "MODIFY",dsts,msg

  def error(self,file,msg):
    print "ERROR",file,msg
    
  def change(self,msg):
    print "CHANGE",msg

  def create(self,msg):
    print "CREATE",msg

ui = Ui()

######################################################################
## relpath
## TODO move out of here, to file or path



######################################################################
## Path

_base_str = str

class Path(_base_str):

  def __repr__(self):
    """ Python presentation of this object. """
    return 'Path(%s)' % _base_str.__repr__(self)

  def __add__(self, more):
    """ Concatenate a string after path specification. """
    return Path(_base_str(self) + more)

  def __radd__(self, other):
    """ Concatenate a string before path specification. """
    return Path(other + _base_str(self))

  def __div__(self,that):
    """ Join a name node to this path. """
    return Path(os.path.join(self,that))

  __truediv__ = __div__

#  def __str__(self):
#    """ Path specification as string. """
#    return self

  ##
  
  def spec(self):
    """ The path specification.
    Returns spec as str.
    """
    return self

  ## 

  def uniq_path(self):
    """ Get the absolute path of the path specification.
    This could require the current working directory
    information getcwd() if relative path.
    """
    return Path(os.path.abspath(self))

  def normcase(self):
    """ Normalize the path specification chracter case to system convention. """
    return Path(os.path.normcase(self))

  def norm_path(self):      
    """ Normalize or compact the path specification. """
    if self == "":
      return Path(".")
    return Path(os.path.normpath(self))

  def real_path(self):
    """ Get the real file location, follow possible symbolic links. 
    Returns path as Path.
    """
    return Path(os.path.realpath(self))

  def expand_user(self):
    """ Substitutes unix user specification by path specification.
    User specification is a tilde ~ or ~user.
    """
    return Path(os.path.expanduser(self))

  def expand_vars(self):
    """ Substitites environment variable specification with the environment
    values.
    Returns path as Path.
    """
    return Path(os.path.expandvars(self))

  def expand(self):
    """ Substitutes user and environment specifications on path.
    """
    return self.expand_vars().expand_user().norm_path()

  ## information 

  def exists(self):
    """ Check if path specification refer to a existing file.
    Returns check as boolean.
    """
    return os.path.exists(self)

  def is_dir(self):
    """ Check if path refers to a directory. """ 
    return os.path.isdir(self)

  def is_reg(self):
    """ Check if path refers to a regular file. """
    return os.path.isfile(self)

  def is_link(self):
    """ Check if path refers to a symbolic link. """
    return os.path.islink(self)

  def is_mountpoint(self):
    """ Check if path refers to a file that is mountpoint. """
    return os.path.ismount(self)

  def can_read(self):
    """ Check if path referring file can be read by the current user. """
    return os.access(self,os.R_OK)

  def can_write(self):
    """ Check if path referring file can be written by the current user """
    return os.access(self,os.W_OK)

  def can_exec(self):
    """ Check if path referring to file can be executed by the current
    process user. """
    return os.access(self,os.X_OK)

  def access_mode(self,follow=True):
    """ The access mode of the file path is referring. """
    if follow:
      mode = os.stat(self)
    else:
      mode = os.lstat(self)    
    return mode.st_mode

  def owner(self):
    """ The owner of the file path is referrring.
    Returns uid as int.
    """
    mode = os.stat(self)
    return mode.st_uid
    
  def group(self):
    """ The group of the file path is referrring.
    Returns gid as int.
    """
    that = os.stat(self)
    return that.st_gid

  def time_create(self):
    """ The creation time of the file path is referring 
    Returns time as int.
    """
    return os.path.getctime(self)

  def time_access(self):
    """ The last accees time of the file path is referring 
    Returns time as int.
    """
    return os.path.getatime(self)

  def time_modify(self):
    """ The last modification time of the file path is referring 
    Returns time as int.
    """    
    return os.path.getmtime(self)
    
  def size(self):
    """ The size of the file the path is referring.
    Returns size as int as bytes.
    """
    return os.path.getsize(self)

  def is_uniq(self):
    """ Is path specification unique (absolute). 
    Returns uniq as boolaen.
    """
    return os.path.isabs(self)

  ## path parts information

  def dir(self):
    """ The directory part of the path. 
    If this path points to root dircetory None is returned.
    """
    if self == os.curdir:
      return Path(os.pardir)
    if self == os.sep: # root, don't go up (unix convention)
      return None
    #if self == os.pardir:
    #  return self.join(os.pardir,os.pardir)
    self_ = self.norm_path()
    nodes = self_.nodes()
    #print ">>>",self,nodes
    if nodes[-1] == os.pardir:
      return self.join(self_,os.pardir)
    return Path(os.path.dirname(self))

  def name(self):
    """ Name part of the path. """
    return os.path.basename(self)

  def ext(self,**kwds):
    """ Extension (type) part of the path.
    Keyword nodot as boolean by default False, if True
    removes leading dot from the ext part.    
    """
    base,ext = self.base_ext(**kwds)
    return ext

  def base(self):
    """ Basename of the path.
    Returns base as str. 
    """
    base,ext = self.base_ext()
    return base

  def drive(self):
    """ The drive specification of the path.
    """
    drive, r = os.path.splitdrive(self)
    return Path(drive)

  def base_ext(self,**kwds):
    """ Get basename and extension of the path. 
    Returns name,ext where name as str and ext as str.
    Keyword nodot as boolean by default False, if True
    removes leading dot from the ext part.
    """
    nodot=kwds.get("nodot",False)
    ##
    name,ext = os.path.splitext(self)
    name = os.path.basename(name)
    if nodot:
      if ext and ext[0] == '.':
        ext = ext[1:]
    return name,ext
      
  def dir_base_ext(self,**kwds):
    """ Get dircetory, basename and extension of the path. 
    Returns dir,name,ext where dir as Path and name as str and ext as str.
    Keyword nodot as boolean by default False, if True
    removes leading dot from the ext part.
    """
    base,ext = self.base_ext(**kwds)
    dir = os.path.dirname(self)
    return Path(dir),base,ext

  def dir_name(self):
    """ Directory and name parts from the path.
    Returns dir,name where dir as Path and name as str.
    """
    dir, name = os.path.split(self)
    return Path(dir), name
  
  def nodes(self):
    """ Get node names from the path specification.
    Returns nodes as list of str.
    """
    if self == '':
      raise SyntaxError("empty path specification")
    nodes = self.split(os.sep)
    if nodes[0] == '': # fix absolute
      nodes[0] = os.sep
    if nodes[-1] == '': # remove trailing slash
      nodes.pop()
    if len(nodes) == 0: # fix
      nodes.append(".")
    #print self," => ",nodes
    return nodes

  def common_path_nodes(self,that):
    """
    Returns common,this_rest,that_rest
    """
    #print "self",self,"that",that
    that_nodes = Path(that).norm_path().nodes()
    this_nodes = self.norm_path().nodes()
    #print this_nodes,that_nodes
    i = 0
    for this_node,that_node in zip(this_nodes,that_nodes):
      if this_node != that_node:
        break
      i += 1
    #print this_nodes[:i],this_nodes[i:],that_nodes[i:]
    return this_nodes[:i], \
           this_nodes[i:], \
           that_nodes[i:]

  def common_path(self,that):
    """
    Returns common,this_rest,that_rest
    """
    common_nodes,this_diff_nodes,that_diff_nodes = self.common_path_nodes(that)
    return self.join(*common_nodes), \
           self.join(*this_diff_nodes), \
           self.join(*that_diff_nodes)

  def join(*names):
    """
    """
    if len(names) < 1:
      return Path("")
    if is_seq(names[0]):
      names = names[0]
    if len(names) < 1:
      return Path("")
    #print "NAMES",names
    return Path(os.path.join(*names))
  join = staticmethod(join)


  def rel_path(self,dst):
    snodes = self.norm_path().nodes()
    dnodes = Path(dst).norm_path().nodes()
    ## case: uniq to rel => simple, return relative
    if snodes[0] == os.sep and dnodes[0] != os.sep:
      return Path(dst).norm_path()
    ## case: rel to uniq => error, no cwd info
    # other possibility is to return uniq
    if snodes[0] != os.sep and dnodes[0] == os.sep:
      #raise ValueError("relative(%s) to unique(%s) request not possible" % (self,dst))
      return Path(dst).norm_path()      
    ##
    if self == os.curdir or self == "":
      return Path(dst).norm_path()
    ##
    rnodes = list() # result
    l = min(len(snodes),len(dnodes))
    i = 0
    ## skip common nodes
    for x in range(0,l):
      if snodes[x] != dnodes[x]:
        break
      i += 1
    ## case uniq to uniq    
    ## case rel to rel
    #print ">>>",snodes[i:],dnodes[i:]
    rnodes.extend([os.pardir] * max(len(snodes) - i,0))
    rnodes.extend(dnodes[i:])
    #print ">>>",Path(self.join(rnodes)).norm_path()
    return Path(self.join(rnodes)).norm_path()
    ## follow
#    si = i
#    di = i
#    while True:
#      if si >= len(snodes) or di >= len(dnodes):
#        break
#      if snodes[si] == os.curdir:
#        si += 1
#        continue
#      if dnodes[di] == os.curdir:
#        di += 1
#        continue
      

      
  def rel_path_XXX2(self,dst):
    common_nodes,this_diff_nodes,that_diff_nodes = self.common_path_nodes(dst)
    this_diff_nodes = [i for i in this_diff_nodes if i != os.curdir]
    that_diff_nodes = [i for i in that_diff_nodes if i != os.curdir]
    diff = len(this_diff_nodes) - len(that_diff_nodes)
    ## uniq to relative, simple return relative
    if len(common_nodes) == 0 and self.is_uniq():
      return dst
    ##
    if diff == 0: #same
      return Path("")
    if len(common_nodes) == 0 and len(that_diff_nodes) == 0: # no rel path
      return Path("")
    elif diff > 0: # self diff longer
      if len(that_diff_nodes) == 0:
        #print common_nodes,this_diff_nodes,that_diff_nodes      
        return self.join([UP] * len(this_diff_nodes))
      else:
        ## no case here ?
        #print self,dst,common_nodes,this_diff_nodes,that_diff_nodes      
        raise NotImplementedError
    else: # dst diff longer
      if len(this_diff_nodes) == 0:
        return self.join(that_diff_nodes)
      else:    
        ## no case here ?
        #print self,dst,common_nodes,this_diff_nodes,that_diff_nodes      
        raise NotImplementedError      

  def rel_path_XXX(self,dst):
    """ relpath(self@string,dst@string) @string, raises ValueError:
    Constructs relative path from self dst dst.
              dst=abs   dst=rel
    self=abs  ok       dst returned
    self=rel  error    self + dst ?
    """
    dst = Path(dst)
    if not self.is_uniq():
      if dst.is_uniq(): # self is rel - dst is abs
        raise ValueError("cannot create relative path from " + self + " to " + dst)
      else:  # self is rel - dst is rel
        return os.path.join(self,dst)
    if not os.path.isabs(dst):
      return dst
    # self is abs, dst is abs
    self = os.path.norm_path(self).split(os.sep)[1:]
    dst = os.path.norm_path(dst).split(os.sep)[1:]
    result = []
    while len(self) and len(dst) and self[0] == dst[0]: 
      self.pop(0); dst.pop(0)
    while len(self) > 0:
      self.pop(0); result.append("..")
    result = os.sep.join(result + dst)
    return result

      

  ############################################################
  ## other
    
  def list(self):
    """ The list of names in this dir.
    """
    if self.is_dir():
      return [Path(p) for p in os.listdir(self)]
    else:
      return self

  def mountpoint(self):
    """ Find the mountpoint under the file is.
    """
    # assumes there is a mountpoint, otherwise hangs
    if self.is_mountpoint():
      return self
    dir = self.dir()
    return dir.mountpoint()
            
  def stat(self,follow=True):
    """ Property information about the file path is referring.
    """
    if follow:
      return os.stat(self)
    else:
      return os.lstat(self)

  def is_match(self,pattern):
    """ Check if path matches to given pattern.
    Returns check as boolean.
    """
    return fnmatch.fnmatch(self, pattern)

  def is_name_match(self,name):
    """ Compare is given name matches matches the path name. """
    return fnmatch.fnmatch(self.name(), pattern)

######################################################################
## Script

class Script(object):
  """ System facade.
  """
  
  def __init__(self,**kwds):
    self.props = dict()
    self.props["follow"] = False
    self.props["depth"]  = True
    self.props["levels"] = None
    self.props["mount"] = True
    self.props["onerror"] = None
    self.props.update(kwds)




  # TODO: better name for "find", find is for searching somthing
  # this if for listing contents on tree structure
  def find_X(self,top,**kwds):
    """
    [onerror] as function(file as Path, exp as Exception) -> go as boolean
    or None.
    If relative path is given, the the processing is depended on
    cwd and changing cwd probable breaks the traversing.
    """
    kwds.setdefault("follow",False) # follow symlinks
    kwds.setdefault("depth",True)   # dir contents first
    kwds.setdefault("levels",None)  # go N dir levels, None == infinite
    kwds.setdefault("mount",True)   # cross the mountpoint
    kwds.setdefault("onerror",None) # action on error
    ##
    if not isinstance(top,Path):
      top = Path(top)
    try:
      start_st = top.stat(follow=kwds["follow"])
    except OSError,e:
      if kwds["onerror"] != None: # if onerror given, let it manage the exc
        kwds["onerror"](top,e)
      else:
        ui.error(top,str(e))
      return      
    ##
    def subfind(top):
      # stop if a symlink and no following
      if top.is_link() and not kwds["follow"]:
        yield(top)
        return
      try:
        st = top.stat(follow=True)
      except OSError,e:
        if kwds["onerror"] != None: # if onerror given, let it manage the exc
          kwds["onerror"](top,e)
        else:
          ui.error(top,str(e))
        return
      # stop is not same device and no cross mounts
      if start_st.st_dev != st.st_dev and not kwds["mount"]:
        yield(top)
        return
      if not top.is_dir():
        yield(top)
      else:
        for name in top.list():
          fullname = top / name
          for path2 in subfind(fullname):
            yield(path2)
        yield(top)
    ## delegate iterarion to caller
    for obj in subfind(top):
      yield(obj)

      
  def cwd(self,path=Void):
    """ Get and set this process current working directory path. """
    if not path is Void:
      path = Path(path)
      if not path.is_dir():
        raise ValueError("%s is not a dircetory" % path)
      ui.change("changing cwd to %s" % path)
      # should dry_run effect ?
      os.chdir(path)
      return path # optimize :)
    return Path(os.getcwd())

  def path(self, *args):
    return Path(os.path.join(*args))

  ## operations

  def copy(self,src,dst):
    """ TODO: """

  def move(self,location):
    """ TODO: """

  def touch(self,file):
    """ Update the modification time to current on give file. """
    ui.modify(file,"updating modification time to current")
    if not cfg_dryrun:
      os.utime(file)
    return file


  def make_file(self,path):
    """ """
    path = Path(path)
    self.make_dir(path.dir())
    log.debug("making file %s" % path)
    self.touch(path)
    # set access
    return path

  def make_file_open(self,path,open_mode):
    """ """
    path = make_file(path)
    log.debug("opening file %s %s" % (path,open_mode))
    if not cfg_dryrun:
      fd = open(path,open_mode)
    else:
      fd = Null
    return fd


  def remove(self,file):
    """ Removes path. If Path is directory it should be
    empty. """
    if not isinstance(file,Path):
      file = Path(file)
    if not file.exists():
      return self
    if file.is_dir():
      if not cfg_dryrun:
        os.rmdir(file)
      ui.remove(file,"directory")
    else:
      if not cfg_dryrun:
        os.remove(file)
      ui.remove(file,"file")
    return self

  def remove_tree(self,path):
    """ XODO: Remove a tree file structure. "rm -rf" """
    pass

  def clean(self,path):
    """ XODO: Clean a path and its empty parents. """
    pass

  def type_indentify(self,file):
    """ XODO: test """
    type,enc = mimetypes.guess_type(file)
    return type
    
  def is_same_filesystem(self,*args):
    """ XODO: test """
    if len(args) == 0:
      return True
    last_dev = None
    for p in args:
      if not isinstance(p,Path):
        p = Path(p)
      try:
        dev = p.stat(follow=False).st_dev
      except OSError,e:
        #print e.errno
        raise e
      if not last_dev == None and last_dev != dev:
        return False
      last_dev = dev
    return True
    
  def is_same_file(self,*args,**kwds):
    """ XODO: test 
    Test if gives paths points to same file. 
    Param args as Path or str. Return boolean.
    Key follow as boolean, defaults True.
    """
    kwds.setdefault("follow",True) # self.ctx.props[]
    if len(args) == 0:
      return True
    last_ino = None
    last_deb = None
    for p in args:
      if not isinstance(p,Path):
        p = Path(p)
      try:
        st = p.stat(follow=kwds["follow"])
      except OSError:
        return False #  not exists cannot be same
      if last_ino != None and last_ino != st.st_ino and last_dev != st.st_dev:
        return False
      last_ino = st.st_ino
      last_dev = st.st_dev
    return True
    
scr = Script()

## TODO: make "ff" as default facade, remove scr and it's dependencies
## ff -- File Functionality
ff = scr

######################################################################
## publish

__all__ = (
  "Path",
  "Script",
  "scr",
  "ff"
)


######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

