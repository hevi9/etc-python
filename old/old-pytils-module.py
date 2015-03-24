#!/usr/bin/env python
## $Id: module.py,v 1.15 2003-10-16 14:09:19 hevi Exp $
## MODULE
## Level 2 software

"""
Python Module management functionality.

root

path: includes extension

file = root + path

qname

roots = sys.path = [root,root,..]

"""
__version__ = "$Revision: 1.15 $"
__docformat__ = "infodoc"
__todo__ = """
"""

from __future__ import generators

if __name__ == '__main__':
  import module
  import sys
  sys.exit(module.check())

######################################################################
## dependencies

import sys
import os
import re
import imp
from inspect import *
import inspect
from pytils.log import log
import parser
import symbol
import token
import pytils.dode
import pytils.rel
import pytils.file

"""
syntax::
ModuleInfo(module_@module)
ModuleInfo(qname@str)
ModuleInfo(qname@str,roots = @seq(str))
ModuleInfo(path@str)
ModuleInfo(path@str,roots = @seq(str))

:module_: Python module.
:qname:   Python dottet module qualified module name specification.
Uses normal module loading rules.
:path:    File system path specification. Can be absolute or relative.
If relative process cwd is used as root. Unsing this does
not give any name for the module.
:roots:   List of roots where to start resolve qname or path.

qname =

root = 

path = root -> path + ext

ext = 

file = root + path + ext 

"""

######################################################################
## utils

# no argument, use _Void as default argument and iffing, when
# default argument might change in run-time
class _Void: pass 

######################################################################
## Module

#class Module(pytils.dode.Dode):
class Module(object):
  """ Development tools information about module. 
  """

  def __init__(self,module):
    assert(inspect.ismodule(module))
    self._module = module
    self._depends = None
    self._qname = None
    self._root = None
    self._path = None
    self._type = None

  def module(self):
    """ Python module.
    + @module
    = pass propterty
    """
    return self._module

  def reload(self):
    """ Reloads module.
    ? Unknown
    = unsync, unsafe
    Todo:
    - implement reloading of the dependends as well.
    """
    assert(type(self._module) == type(os))
    reload(self._module)

  def update(self):
    if self._depends == None:
      log.debug("updating module dependencies",self.source())
      self._depends = pytils.rel.union(self.depends_runtime(),
                                      self.depends_fromfile())
    self._update_location()

  def _update_location(self):
    src = self.source()
        
  def name(self):
    """ Name of the module (not a qname). Use if this is a bit
    questinable as this is no way unique name for the module.
    By this name the module cannot be accessed again.
    + @str Simple name of the module.
    ? None
    = readonly
    = safe
    """
    info = inspect.getmoduleinfo(self._module.__file__)
    assert(info)
    return info[0]
  
  def source(self): # == file
    """ Source file (root + path) of the module.
    + path@str|None source path or None if no source file available.
    ? Unknown
    = unsafe
    """
    srcfile = None
    if hasattr(self._module,"__file__"):
      info = inspect.getmoduleinfo(self._module.__file__)
      if info == None:
        pass
      elif info[3] == imp.PY_SOURCE:
        srcfile = self._module.__file__
      elif info[3] == imp.PY_COMPILED:
        srcfile = self._module.__file__
        path,ext = os.path.splitext(srcfile)
        srcfile = path + ".py"
        if not os.path.exists(srcfile):
          srcfile = None
      elif info[3] == imp.C_EXTENSION:
        pass
      elif info[3] == imp.PY_RESOURCE:
        pass
      else:
        raise RuntimeError("should not happen")
    return srcfile

  def depends_runtime(self):
    """ Find module dependencies to other module at runtime.
    This does not reveal all modules. Import format::
    from pytils.log import log
    is problematic because just imported object may not be able
    to produce information, that in what module it is defined.
    """
    modules = dict() # dependent module set
    for name,object in inspect.getmembers(self._module):
      module_o = inspect.getmodule(object)
      if module_o == None:
        continue
      if module_o == self._module: # object defined in module
        continue
      modules[module_o] = 1
    return modules.keys()

  def depends_fromfile(self):
    """ Find module dependencies from the file.
    """
    log.debug(self.name(),"finding dependencies from source",self.source())
    modules = list()
    file = self.source()
    if file == None:
      modules
    source = open(file).read()
    try:
      ast = parser.suite(source)
    except parser.ParserError,msg:
      raise SyntaxError(file + ":" + str(msg))
    ## 
    def get_token(root,toknum):
      if root[0] == toknum:
        return root
      for i in root:
        if type(i) == tuple:
          ret = get_token(i,toknum)
          if ret != None:
            return ret
      return None
    ## get qname as list
    def handle_import(stmt):
      qname = list()
      for i in get_token(stmt,symbol.dotted_name)[1:]:
        if i[0] == token.NAME:
          qname.append(i[1])
          assert(len(qname) > 0)
      return qname
    ## find imports
    def walk(root):
      for i in range(0,len(root)):
        if token.ISNONTERMINAL(root[i]):
          if root[i] == symbol.import_stmt:
            modules.append(handle_import(root))
            return
          if type(root[i]) == tuple:
            walk(root[i])
    walk(ast.totuple())
    ## remove duplicates
    module_set = dict()
    for i in modules:
      module_set[".".join(i)] = 1
    return module_set.keys()

  def depends(self):
    self.update()
    return self._depends


  def _future_root(self):
    """ Root of the module """
    pass

  def _future_path(self):
    """ Path of the module """
    pass

######################################################################
## Importer

class Importer(object):
  """ Module importer.
  """

  def __init__(self):
    pass

  def import_qname(self,qname):
    """ Import module by dotted python name path (qname).
    Relates to the sys.path.
    - qname@str dottet module name
    + module@module return module object
    ? unknown
    = unsafe
    """
    ## import module
    module = None
    if qname in sys.modules:
      module = sys.modules[qname]
    else:
      try:
        module = __import__(qname)
      except ImportError, e:
        log.error("cannot load module:","\"" + qname + "\"",":" + str(e))
        raise ImportError(str(e) + " for " + qname)   
      except ValueError, e:  
        log.error("cannot load module:","\"" + qname + "\"",":" + str(e))
        raise ValueError(str(e) + " " + qname)   
      try:
        for part in string.split(qname,'.')[1:]:
          module = getattr(module,part)
      except AttributeError,e:
        log.error("no module found: ","\"" + qname + "\"",":" + str(e))
        raise AttributeError(str(e) + " " + qname)   
    ## wrap
    return module

  def import_path(self,path):
    """ Import module by given file path.
    This is not yet fully correct, this imports module as qname
    after all, not as a direct file.
    - path@str Path to file, can be relative or absolute.
    + module@Module Imported module.
    ? unknown
    = unsafe
    """
    qname = self.path2qname(path)
    log.info("importing path",path,"as",qname)
    return self.import_qname(qname)

  def import_path_noname(self,path):
    """ import unnamed module direcly from given path
    """
    pass

  def find_module(self,qname,rootpath = _Void): # find_module_qname
    """
    Find python module file information for given qname. This
    uses sys.path for root location and search order is according that.
    Gives priority for modules (files) in search (over packages/directories).
    - qname@str Module qualified name specification.
    - rootpath@list(@str) Optional module root path.
    + root@str|None Root where module is found.
    + path@str|None Path (filename) to the module from the root.
    + type@str|None Type of module, see imp.get_suffixes().
    = safe
    = readonly
    ? None
    """
    if rootpath == _Void: # set the rootpath to syspath as default
      rootpath = sys.path # no default argument as it gets fixed at compile
    parts = qname.split(".")
    for root in rootpath:
      path = os.path.join(*parts)
      ## test for module file
      for ext in imp.get_suffixes():
        path_ext = path + ext[0]
        if os.path.exists(os.path.join(root,path_ext)):
          return root,path_ext,ext[2]
      ## test for package directory
      if (os.path.exists(os.path.join(root,path)) and
          os.path.isdir(os.path.join(root,path))):
        path2 = os.path.join(path,"__init__")
        for ext in imp.get_suffixes():
          path2_ext = path2 + ext[0]
          if os.path.exists(os.path.join(root,path2_ext)):
            return root,path2_ext,ext[2]
    return None,None,None
    
  def split_module_file(self,file,rootpath = _Void):
    """ Split absolute module file spesification into parts.
    - file
    + root
    + path
    + type
    """
    if rootpath == Void:
      rootpath = sys.path
    for root in rootpath:
      if os.path.commonprefix((root,file)) == root:
        path = file[len(root):]
        
    

  def find_moduleFiles(self,root):
    """ Find all python module files under given root. Does not
    note symlinks, so symlinks are followed (or handled as file
    on that place). If both source and compiled files exists, gives
    source file. Gives shared objects ay case are they python
    extensions or not.
    - root@str 
    + paths@list(str) List pf paths to module files relative to the
      given root.
    ? unknown
    = safe
    = readonly
    """
    return self._find_moduleFiles(root)

  def find_sub_moduleFiles(self,root,subpath):
    """ Find python module files under given root and subdirectory.
    - root@str
    - subpath@str
    + paths@list(@str)
    ? unknown
    = safe
    = readonly
    """
    subroot = os.path.join(root,subpath)
    return self._find_moduleFiles(subroot)

  def _find_moduleFiles(self,root):
    files = list()
    for path in pytils.file.treelistdir(root):
      type = self.filetype(root,path)
      if type != None:
        if type == imp.PY_COMPILED:
          name,ext = os.path.splitext(path)
          name = os.path.join(root,name + ".py")
          if not os.path.exists(name):
            files.append(path)
        else:
          files.append(path)
    return files

  

  def filetype(self,root,path):
    """
    - root
    - path
    + imp.PY_SOURCE,|imp.PY_COMPILED|imp.C_EXTENSION|None, where
      PY_SOURCE The module was found as a source file
      PY_COMPILED The module was found as a compiled code object file.
      C_EXTENSION  The module was found as dynamically loadable shared
      library.
    = safe
    = readonly
    """
    suffixes = dict()
    for desc in imp.get_suffixes():
      suffixes[desc[0]] = desc
    name,ext = os.path.splitext(path)
    if ext in suffixes:
      return suffixes[ext][2] # (ext,openmode,type)
    else:
      return None # not a python file

  def path2qname(self,path):
    """ Changes relative file path specification to the python
    module (or package) qname.
    - path@str
    + qname@str
    = safe
    = readonly
    ? none
    """
    name,ext = os.path.splitext(path)
    parts = name.split(os.sep)
    if parts[-1] == '__init__':
      del parts[-1]
    name = ".".join(parts)
    return name
  

# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

