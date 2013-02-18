"""
Wrapper over subprocess module to specify
and declared used programs in code.

Usage::

  from hevi_proto.program import Program, manifest
  
  ls = Program("ls","-la")
  
  ls()
  ls("-tr")
  
  ..
  
  print("Used programs:")
  for p in manifest():
    print("  {}".format(p.name))
"""

##############################################################################
## 

import subprocess
import logging
log = logging.getLogger(__name__)

##############################################################################
## module

__manifest = list()

def _manifest_insert(p):
  assert p not in __manifest
  __manifest.append(p)

def manifest():
  return __manifest

##############################################################################
## Program

class Program:
  
  def __init__(self,*args,**kwds):
    _manifest_insert(self)
    log.debug(*args)
    self._args = args
    log.debug(self._args)

  def __call__(self,*args,**kwds):
    cmdargs = self._args + args
    log.debug(" ".join(cmdargs))
    
  @property
  def name(self):
    return self._args[0]
    

##############################################################################
## test

if __name__ == "__main__":
  from hevi_proto.program import Program, manifest
  ls = Program("ls","-la")
  ls()
  ls("-tr")
  print("Used programs:")
  for p in manifest():
    print("  {}".format(p.name))
