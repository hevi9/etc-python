#!/usr/bin/env python
## $Id: load.py.no,v 1.1 2003-07-17 13:13:31 hevi Exp $
##
## TODO
## - clean up
## - docs
## - recursive modules
## * problem: if there is bin/run.py modele and run/ package in
##   module tree. bin/run.py is loaded instead run/ package
## - see pydoc safeloader

"""
"""
__version__ = "$Revision: 1.1 $"
__todo__ = """
4 #file backup file management
"""

#module pytils.load
#import sys
#import os
#from os import path
#from pytils.log import log
#from pytils.rel import *
#import pytils
#import re
#import imp
#from inspect import *
#
#######################################################################
#
#
#
#
#def findModuleFiles(root):
#  """ findModuleFiles(root@str) @list(str):
#  - recursive
#  """
#  moduleFiles = {}
#  def walk(root,file): # root abs, file rel
#    absfile = path.normpath(path.join(root,file)) # make abs
#    if path.isdir(absfile):
#      for infile in os.listdir(absfile):
#        subfile = path.normpath(path.join(file,infile)) # relative to subroot
#        walk(root,subfile)
#    else:
#      name,ext = path.splitext(file)
#      if ext in (".py",".pyc",".pyo"):
#        if path.basename(name) in ("__init__",): # ignore
#          return
#        moduleFiles[file] = 1
#  walk(root,".")
#  return moduleFiles.keys()
#
#def file2name(file):
#  """ file2name(file@str)@str:
#  Translate the relative filename file of the module to the python
#  dottet module path name.
#  Returns translated name.
#  """
#  name,ext = path.splitext(file)
#  name = ".".join(string.split(name,"/"))
#  return name
#
#
#def exports(rootobj):
#  objs = {}
#  def walk(robj):
#    for obj in robj.__dict__.values():
#      pass
#
#    def walk(obj,name = None):
#      if not (inspect.ismodule(obj) or
#          inspect.isclass(obj) or
#          inspect.ismethod(obj) or
#          inspect.isfunction(obj) or
#          inspect.isbuiltin(obj)):
#        return
#      self.objs[obj] = name
#      if name != None:
#        if name[0] != '_':
#          self.names[name] = obj
#      if inspect.ismodule(obj) or inspect.isclass(obj): # namespace
#        for subname in dir(obj):
#          subobj = getattr(obj,subname)
#          if subobj in self.objs.keys(): continue
#          walk(subobj,subname)
#    for module in self.modules.keys():
#      walk(module)
#
#######################################################################
#
#def findModules2(dirs):
#  """ findModules(dirs [str]) [str]:
#  dirs: directories to look modules
#  returns: list of module names
#  """
#  def ispy(file): # simple
#    list = re.split(r'\.',os.path.basename(file))
#    if list[-1] == "py":
#      return file
#    return None
#  def tomod(file): # simple
#    list = re.split(r'\.',os.path.basename(file))
#    return ".".join(list[0:-1])
#  result = []
#  for dir in dirs:
#    result += map(tomod,filter(ispy,os.listdir(dir)))
#  return result
#
#def loadModules(names,dirs):
#  """ loadModules(names [str],dirs [str]) [module]:
#  names: list(seq?) of module names
#  dirs: list(seq?) of directories
#  returns: list of modules 
#  """
#  modules = []
#  for name in names:
#    #log.debug("loading",name)
#    if name in sys.modules: # should check dirs ?
#      modules += sys.modules[name]
#      log.debug("module",name,"already loaded")
#      continue
#    fp = None
#    try:
#      fp,path,desc = imp.find_module(name,dirs)
#      module = imp.load_module(name,fp,path,desc)
#      #module = __import__(name,globals(),locals())
#      modules.append(module)
#    except ImportError, e:
#      log.error("cannot load module",name,e)
#    if fp: fp.close()
#  return modules
#
#
#def instancesInDirs(dirs,klasses):
#  """ instancesInDirs(dirs [str],klasses [class]) [object]:
#  Return instancies of classes matching klasses in modules on dirs.
#  """
#  names = difference(findModules(dirs),["__init__"])
#  modules = loadModules(names,dirs)
#  return findInstancesOf(modules,klasses)
#
#
#######################################################################
### - pkgdir
### - sys.path
### - superclass
### from dir as pkg conforming to superclass
#
#class Loader2:
#
#  def __init__(self,pkg):
#    """
#    """
#    self.pkg = pkg
#    self.modules = []
#    self.names = []
#    self.moddir = None
#    self._loadModules()
#
#  def _findModules(self):
#    # resulve the root for modules
#    pkgpath = os.path.join(re.split(r'\.',self.pkg))
#    moddir = None
#    for root in sys.path:
#      dir = os.path.join(root,*pkgpath)
#      if os.path.isdir(dir):
#        moddir = dir
#        break
#    if moddir:
#      log.debug("using " + moddir)
#      self.moddir = moddir
#    else:
#      log.error(self.pkg + " does not found in syspath")
#      return [] # on None ?
#    modules = []
#    def walk(subroot):
#      subrootfile = os.path.normpath(os.path.join(moddir,subroot))
#      if os.path.isdir(subrootfile):
#        for file in os.listdir(subrootfile):
#          subfile = os.path.normpath(os.path.join(subroot,file))
#          walk(subfile)
#      else:
#        name,ext = os.path.splitext(subroot)
#        if ext in (".py",".pyc",".pyo"):
#          name = ".".join(re.split(r'\.',name))
#          if name == "__init__":
#            return
#          self.names.append(os.path.join([self.pkg,name]))
#          modules.append(".".join([self.pkg,name]))
#    walk(".")
#    return compact(modules)
#      
#  def _loadModules2(self):
#    for moduleName in self._findModules():
#      if moduleName in self.modules:
#        continue
#      if moduleName in sys.modules:
#        self.modules.append(sys.modules[moduleName])
#        log.debug("module",moduleName,"already loaded")
#        continue
#      try:
#        #print moduleName, self.moddir
#        module = None
#        #module = __import__(moduleName,globals(),locals())
#        #module = __import__(moduleName,globals(),locals(),None)
#        #fp,path,desc = imp.find_module(moduleName,sys.path)
#        #print path
#        #module = imp.load_module(moduleName,fp,path,desc)
#        
#        self.modules.append(module)
#      except ImportError, e:
#        log.error("cannot load module: ",moduleName,e)
#
#  def _loadModules(self):
#    self._findModules()
#    for file in self.names:
#      #print file
#      pass
#
#  def instancesOf(self,klasses):
#    """
#    """
#    insts = []
#    for module in self.modules:
#      for name in dir(module):
#        value = getattr(module,name)
#        for klass in klasses:
#          if isinstance(value,klass):
#            insts.append(value)
#            log.debug("got",value,"in",value.__module__)
#            break
#    return insts
#
#######################################################################
###
#
#class Loader:
#  def __init__(self,dir):
#    self.dir = dir
#    self.modules = []
#    self._load()
#
#  def _load(self):
#    def walk(rfile):
#      afile = os.path.normpath(os.path.join(self.dir,rfile))
#      if os.path.isdir(afile):
#        for file in os.listdir(afile):
#          walk(os.path.join(rfile,file))
#      else:
#        name,ext = os.path.splitext(rfile)
#        if ext in (".py",):
#          name = os.path.normpath(name)
#          if name == "__init__":
#            return
#          fh = None
#          try:
#            fh = open(afile,"r")
#            module = imp.load_module(name,fh,afile,('.py', 'r', 1))
#            self.modules.append(module)
#          except ImportError, e:
#            log.error("cannot load module: ",name,afile,e)
#          if fh: fh.close()
#    walk(".")
#
#  def instancesOf(self,klasses):
#    """
#    """
#    insts = []
#    for module in self.modules:
#      for name in dir(module):
#        value = getattr(module,name)
#        for klass in klasses:
#          if isinstance(value,klass):
#            insts.append(value)
#            log.debug("got",value,"in",value.__module__)
#            break
#    return insts
#
#
#######################################################################
#
#      
#
#######################################################################
### checking
### - load 
#
#
#def check1():
#  log.addWriter(mod.log.LogDefault())
#  rundir = os.path.join(os.environ["HOME"],"pse","run")
#  names = difference(findModules([rundir]),["__init__"])
#  modules = loadModules(names,[rundir])
#  import run.base
#  import run.b
#  import bin.pse
#  findInstancesOf(modules,[run.base.A,bin.pse.Runner])
#
#def check2():
#  log.addWriter(mod.log.LogDefault())
#  l = Loader("/home/hevi/pse/run")
#        
#if __name__ == '__main__':
#  for arg in sys.argv[1:]:
#    if arg in globals().keys():
#      apply(globals()[arg])
#    
## Local Variables:
## mode: python
## mode: auto-fill
## fill-column: 79
## fill-prefix: "  "
## indent-tabs-mode: nil
## py-indent-offset: 2
## End:

