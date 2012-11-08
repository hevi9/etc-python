"""
Utilities collection
********************

PropsDict
=========

Iterable entry point for class properties. Properties
in enrty are readonly.

Usage::
  from util import PropsDict
  ..
  class MyData:
    def __init__(self):
      self.props = PropsDict(self)
      self._data = "value"
    @property
    def data(self):
      return self._value
  ..
  obj = MyData(
  for key in obj:
    print("{0} = {1}".format(key,obj.props[key])
    
f is for a format
=================

Convience format function that takes format keys directly
from locals and globals.

Usage::
  from util import f
  ..
  b = 100
  def func():
    a = "value"
    log.debug(f"{a} and {b}")
    
CUI
===
"""

##############################################################################
## Uses & Setup

import collections # http://docs.python.org/release/3.2.3/library/collections.html
import inspect # http://docs.python.org/release/3.2.3/library/inspect.html
import argparse # http://docs.python.org/py3k/library/argparse.html
import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
__all__ = list()

##############################################################################
## PropsDict

class PropsDict(collections.Mapping):
  
  def __init__(self,obj,pred=lambda m: isinstance(m,property)):
    self._obj = obj
    self._keys = list()
    for key, value in inspect.getmembers(obj.__class__, pred):
      self._keys.append(key)
    
  def __getitem__(self,key):
    if key in self._keys:
      return getattr(self._obj,key)
    else:
      raise KeyError(key)
  
  def __iter__(self):
    for key in self._keys:
      yield key
  
  def __len__(self):
    return len(self._keys)

__all__.append("PropsDict")


##############################################################################
## f is for format

def f(s):
  """ Format text from locals and globals names. """
  caller = inspect.currentframe().f_back
  combi = dict(caller.f_globals)
  combi.update(caller.f_locals)
  return s.format(**combi)
__all__.append("f")

##############################################################################
## CUI

class CUI:
  """ """

  def __init__(self):
    ## handle command line arguments
    self.parser = argparse.ArgumentParser(
      description=""" CUI """,
      epilog="\n"
      )
    ## declare options
    self._init_args()
    ## parse command line args
    self.args = self.parser.parse_args() ### !!!
    ## setup logging
    logging.basicConfig()
    if self.args.debug:
      logging.getLogger().setLevel(logging.DEBUG)
    elif self.args.quiet:
      logging.getLogger().setLevel(logging.WARNING)
    else:
      logging.getLogger().setLevel(logging.INFO)

  def _init_args(self):
    self.parser.add_argument("param",
      nargs="*",
      help="parameters")
    self.parser.add_argument("--debug",
      action="store_true",
      help="Activate debugging output")
    self.parser.add_argument("--quiet",
      action="store_true",
      help="Disable informatic logging")

__all__.append("CUI")
