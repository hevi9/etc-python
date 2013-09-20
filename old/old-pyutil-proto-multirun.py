#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id$
## MODULE

assert False,"Not for use"

"""
"""
__version__ = "$Revision$"
__docformat__ = "plaintext"

######################################################################
## dependencies

import os
import re
from pyutil.script import Script,Path
import fnmatch as fnm
import logging as log
import pyutil.module as mdl
import time

scr = Script()

######################################################################
## config

class cfg(object):
  dry_run = False

######################################################################
## Part

class Void: pass

class Part(object):
  
  def __init__(self):
    self._command = None
  
  def order(self,value=Void):
    if value != Void:
      assert value > 0 and value <= 99
      self._order = value
    return self._order

  def context(self,value=Void):
    if value != Void: self._context = value
    return self._context

  def subject(self,value=Void):
    if value != Void: self._subject = value
    return self._subject

  def command(self,value=Void):
    if value != Void: self._command = value
    return self._command

  def file(self,value=Void):
    if value != Void: self._file = value
    return self._file

  def has_cmd(self,cmd):
    return False

  def run(self,cmd):
    return False

######################################################################
## InitPart

class InitPart(Part):
  
  def has_cmd(self,cmd):
    return True

  def run(self,cmd):
    rcmd = "%s %s" % (self.file(),cmd)
    log.debug("InitPart.run: %s" %rcmd)
    if cfg.dry_run:
      return True
    rc = os.system(rcmd)
    if os.WEXITSTATUS(rc) != 0:
      return False
    else:
      return True

######################################################################
## PyPart
  
class PyPart(Part):

  def __init__(self):
    self._module = None
    self._commands = None # map: command => callable
    
  def load(self):
    self._module = mdl.import_anon_file(self.file())
    try:
      self._commands = self._module.commands()
    except AttributeError:
      self._commands = None
        
  def has_cmd(self,cmd):
    return self._commands != None and self._commands.has_key(cmd)

  def run(self,cmd):
    log.debug("PyPart.run: %s %s" % (self.file(),cmd))    
    if cfg.dry_run:
      return True
    if not self._commands:
      log.debug("%s has no commands" % self.file())
      return False
    rcmd = self._commands[cmd]
    return rcmd()
    
######################################################################
## CmdPart
  
class CmdPart(Part):
  
  def has_cmd(self,cmd):
    if cmd == self.command():
      return True
    return False

  def run(self,cmd):
    rcmd = "%s" % self.file()
    log.debug("CmdPart.run: %s" %rcmd)
    if cfg.dry_run:
      return True
    rc = os.system(rcmd)
    if os.WEXITSTATUS(rc) != 0:
      return False
    else:
      return True    

######################################################################
## Multirun

class Multirun(object):
  
  def __init__(self,**kwds):
    self.dir = Path(kwds["dir"])
    self.prefix = kwds["prefix"]
    self.ignore = kwds["ignore"]
    ##
    self._all = list()
    self._all_py = list()
    ##
    self._load()
        
  def run(self,cmd):
    all_sorted = filter(lambda x: x.has_cmd(cmd),self._all)
    all_sorted.sort(lambda x,y:cmp(x.order(),y.order()))
    log.debug("running: %s %d/%d" % (cmd,len(all_sorted),len(self._all)))
    start_time = time.time()
    for part in all_sorted:
      succ = part.run(cmd)
      if not succ:
        log.error("%s: %s failed" % (cmd,part.file()))
    log.debug("used time %f" % (time.time() - start_time))

  def list(self):
    return self._all
      
  def list_files(self):
    rl = list()
    for part in self._all:
      rl.append(part.file())
    return rl

  def _load(self):
    for name in self.dir.list():
      if self.is_ignorable(name):
        continue
      if not self.is_wanted(name):
        continue
      ##
      file = self.dir/name
      name,ext = file.base_ext(nodot=True)
      np = name.split('-')
      part = None
      if len(np) == 5: # with command
        if ext == 'py' and np[4] == 'mod':
          part = PyPart()
          self._all_py.append(part)
        else:
          part = CmdPart()
          part.command(np[4])          
        part.order(int(np[1]))
        part.context(np[2])
        part.subject(np[3])
      elif len(np) == 4: # no specific command
        part = InitPart()
        part.order(int(np[1]))
        part.context(np[2])
        part.subject(np[3])
      else: # error
        raise SyntaxError("error in %s" % name)        
      part.file(file)
      self._all.append(part)        
    ##
    self._load_mods()
    
  def _load_mods(self):
    for pypart in self._all_py:
      pypart.load()
                
  def is_ignorable(self,name):
    for ignore_glob in self.ignore:
      #print ignore_glob
      if fnm.fnmatch(name,ignore_glob):
        log.debug("ignoring %s",name)
        return True
    return False
    
  def is_wanted(self,name):
    if name.startswith(self.prefix):
      return True
    return False

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:

