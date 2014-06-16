
import logging
from _collections import deque
log = logging.getLogger(__name__)
D = log.debug

##############################################################################

class Item:
  def __init__(self):
    self.default = None # Value
  
class Group(Item):
  
  def __init__(self):
    super().__init__()
    self._data = dict()
    self.default = self
  
class Schema:
  
  def __init__(self):
    self._ctrl = None
    self._data = dict()

  def ctrl(self):
    if not self._ctrl:
      self._ctrl = Ctrl(self)
    return self._ctrl

  def __call__(self, name, default, *, vtype=None, doc=None):
    if vtype is None:
      vtype = type(default)    
    ##
    path = deque(name.split("."))
    D("name=%s (path=%s) default=%s vtype=%s doc=%s", name, path, default, vtype, doc)
    group = self    
    while len(path) > 1:
      name = path.popleft()
      if not name in group._data:
        group1 = Group()
        group._data[name] = group1
      group = group._data[name]        
    ##
    item = Item()
    item.name = name
    item.default = default
    item.vtype = vtype
    item.doc = doc
    group._data[name] = item
    
class Ctrl:

  def __init__(self, schema):
    D("__init__ %s", schema)
    self.__schema__ = schema
    self.__data__ = dict()

  def __getattr__(self, key):
    D("__getattr__ %s", key)
    if key in self.__data__:
      return self.__data__[key]
    elif key in self.__schema__._data:
      return self.__schema__._data[key].default
    else:
      return self.__dict__[key]

  def __setattr__(self, key, value):
    D("__setattr__ %s %s", key, value)
    self.__dict__[key] = value
  

##############################################################################

logging.basicConfig(level=logging.DEBUG)

schema = Schema()
schema("debug", False, doc = """
Testing """)
schema("args.verbose", 2)

ctrl = schema.ctrl()

print("-"*80)
print(dir(ctrl))
print("-"*80)
print("ctrl.debug =",ctrl.debug)
ctrl.debug = True
print("ctrl.debug =",ctrl.debug)
print("-"*80)
print("ctrl.args.verbose =", ctrl.args.verbose)


