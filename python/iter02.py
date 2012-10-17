""" 
"""

import collections # http://docs.python.org/release/3.2.3/library/collections.html
import inspect # http://docs.python.org/release/3.2.3/library/inspect.html

class PropsMixin:
  
  def props(cls): pass
  def _propsget(cls):
    pass
  props.__get__ = _propsget

    
##############################################################################
##

class Test(PropsMixin):
  
  def __init__(self):
    self.objdata = "OBJVALUE"
  
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
