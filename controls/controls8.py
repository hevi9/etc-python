
import logging
from collections import deque
log = logging.getLogger(__name__)
D = log.debug

##############################################################################

LOGFORMAT = "[%(levelname)s|%(filename)s:%(lineno)s|%(funcName)s] %(message)s"

##############################################################################

class _Base:
  
  def __init__(self, schema=None, name=None):
    if name is not None:
      assert not name.startswith("_")
    self.__schema = schema
    self.__name = name
    D("new: %s[0x%08x] name=%s", self.__class__.__name__, id(self), name)

  @property
  def name(self):    
    return self.__name if self.__name is not None else "<ROOT>"
  
  @property
  def schema(self):
    return self.__schema
  
  @property
  def root(self):
    return self if self.__schema is None else self.root    
  
  @property
  def is_schema(self):
    return False
  
  @property
  def nodepath(self):
    return self.__schema.nodepath + [self.__name] if self.__name is not None else []

  @property
  def path(self):
    return ".".join(self.nodepath)

##############################################################################

class _Item(_Base):
  
  def __init__(self, schema,  name, vdefault, *, doc=None, vtype=None):
    super().__init__(schema, name)
    self.vdefault = vdefault
    self.vtype = vtype
    self.doc = doc
    
    
##############################################################################

class _Schema(_Base):
  
  def __init__(self, schema=None, name = None):
    super().__init__(schema, name)
    self.__items = dict()
    
  def __call__(self, namepath, vdefault):
    D("dcl: %s <= %s=%s", self.name, namepath, vdefault)
    ## handle dottet name path
    path = namepath.split(".")
    if len(path) > 1:
      if path[0] in self.__items:
        schema = self.__items[path[0]]
      else:
        schema = _Schema(self, path[0])
        self.__items[path[0]] = schema
      if not isinstance(schema, _Schema):
        raise AttributeError(
          "'{}' assigned as schema group, but is alread declared to '{}'".
          format(path[0], self.__items[path[0]].vdefault))
      schema(".".join(path[1:]), vdefault) # sub declaration
    else:
      item = _Item(self, path[0], vdefault)
      self.__items[path[0]] = item
      
  @property
  def items(self):
    for key in self.__items:
      yield self.__items[key]
    
  @property
  def is_schema(self):
    return True
  
  def get(self, key):
    return self.__items[key]

##############################################################################
    
class Ctrl:

  def __init__(self, schema):
    D("new: %s[0x%08x]", self.__class__.__name__, id(self))
    self.__schema = schema

  def __getattr__(self, key):
    D("__getattr__ %s", key)
    try:
      return object.__getattribute__(self, key)
    except AttributeError as ex:
      try:
        item = self.__schema.get(key)
        if item.is_schema:
          ctrl = Ctrl(item)
          self.__dict__[key] = ctrl
          return ctrl 
        else:
          return item.vdefault
      except KeyError as ex:        
        raise AttributeError("Key '%s' not in control values or not declared in schema" % ex.args[0])

  def __setattr__(self, key, value):    
    # guard for __*
    if key.startswith("_Ctrl") or key.startswith("__"):
      self.__dict__[key] = value
    else:
      item = self.__schema.get(key) # XXX
      D("%s=%s", item.path, value)
      self.__dict__[key] = value
  
  def __iter__(self):
    return iter(self.__dict__)

  def __getitem__(self, key):
    return self.__dict__[key]
  
##############################################################################

class _RootSchema(_Schema):
  
  def __init__(self):
    super().__init__()
    self.__ctrl = Ctrl(self)

  def get_control(self):
    return self.__ctrl

__prog_schema = None

def prog_schema():
  global __prog_schema
  if __prog_schema is None:
    __prog_schema = _RootSchema()
  return __prog_schema
    
##############################################################################

def fill(s):
  s("test", 1001)
  #s("test.nowork",1)
  s("group.test", 2002)
  s("group.joo", "jeejee")
  s("group.group.name","dvalue")

def run1():
  schema = prog_schema()
  fill(schema)
  ctrl = schema.get_control()
  print(ctrl.group.group.name)
  ctrl.group.group.name = "New Name"
  print(ctrl.group.group.name)
  

if __name__ == "__main__":
  logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
  run1()

