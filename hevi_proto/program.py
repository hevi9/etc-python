"""
hevi_util.program
=================

Wrapper over subprocess module to specify
and declared used programs in code.

Usage::

  from hevi_proto.program import Program, manifest
  
  ls = Program("ls","-la")
  
  ls()
  ls("-tr")
  
  print("Used programs:")
  for p in manifest():
    print("  {}".format(p.name))
"""

##############################################################################
## 

import subprocess # http://docs.python.org/3/library/subprocess.html
import logging # http://docs.python.org/3/library/logging.html
import os # http://docs.python.org/3/library/os.html
log = logging.getLogger(__name__)
j = os.path.join

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
  
  def __init__(self,*args):
    _manifest_insert(self)
    self._args = args

  def __call__(self,*args,**kwds):
    cmdargs = self._args + args
    log.debug(" ".join(cmdargs))
    return subprocess.check_call(cmdargs,**kwds)
    
  @property
  def name(self):
    return self._args[0]
    
  @property
  def args(self):
    return self._args
    
  @property
  def which(self):
    # absolute
    if os.path.isabs(self.name):
      return self.name
    # relative path
    name = os.path.basename(self.name)
    if name != self.name:
      return self.name
    # just name
    for dir in os.environ["PATH"].split(":"):
      if os.access(j(dir,self.name), os.X_OK):
        return j(dir,self.name)
        break
    return None
    

##############################################################################
## test

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  from hevi_proto.program import Program, manifest
  ls = Program("ls","-la")
  false = Program("false")
  notfound = Program("notfound")
  ls()
  ls("-tr",shell=True)
  try:
    false()
  except subprocess.CalledProcessError as ex:
    pass
  try:
    notfound()
  except OSError as ex:
    pass
  print("Used programs:")
  for p in manifest():
    print("  {} ({})".format(p.name,p.which))
