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
"""

##############################################################################
## Uses & Setup

import collections # http://docs.python.org/release/3.2.3/library/collections.html
import inspect # http://docs.python.org/release/3.2.3/library/inspect.html
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