""" 
"""

import collections # http://docs.python.org/release/3.2.3/library/collections.html
import inspect # http://docs.python.org/release/3.2.3/library/inspect.html

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
    
##############################################################################
##

class Test:
  
  def __init__(self):
    self.objdata = "OBJVALUE"
    self.props = PropsDict(self)
  
  @property
  def data1(self):
    return "VALUE1"

  @property
  def data2(self):
    return "VALUE2"
  

test = Test()
print("test.data1 = {0}".format(test.data1))
print("test.data2 = {0}".format(test.data2))
print("test.props['data1'] = {0}".format(test.props["data1"]))
print("test.props['data2'] = {0}".format(test.props["data2"]))
print("iteration")
for prop in test.props:
  print("  {0} = {1}".format(prop,test.props[prop]))
for prop in test.props.values():
  print("  {0}".format(prop))


