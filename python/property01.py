"""
Properties usage

http://stackoverflow.com/questions/2390827/how-to-properly-subclass-dict-and-override-get-set

"""

class propdict(dict):
  
  def __init__(self,obj):
    self._obj = obj
    
  def __getitem__(self, key):
    return getattr(self._obj,key)

  def __contains__(self, key):
    return hasattr(self._obj,key)
  
  def __iter__(self, *args, **kwargs):
    return dict.__iter__(self, *args, **kwargs)

class A:
  
  def __init__(self):
    self._value = "VALUE"
    self.props2 = propdict(self)
    
  
  @property
  def prop(self):
    return self._value
  
  props = dict()
  
a = A()
print("a.prop = {0}".format(a.prop))
print("A.prop = {0}".format(A.prop))
print("A.prop.__get__(a) = {0}".format(A.prop.__get__(a)))

print("a.props['prop'] = {0} ".format(a.props2["prop"]))

for key in a.props2:
  print(a.props[key])