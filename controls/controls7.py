
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
    self._schema = schema
    self._name = name
    D("new: %s[0x%08x] name=%s", self.__class__.__name__, id(self), name)

  @property
  def name(self):    
    return self._name if self._name is not None else "<ROOT>"
  
  @property
  def schema(self):
    return self._schema
  
  @property
  def root(self):
    return self if self._schema is None else self.root    
  
  @property
  def is_schema(self):
    return False

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
    self._items = dict()
    
  def __call__(self, namepath, vdefault):
    D("assign: %s <= %s=%s", self.name, namepath, vdefault)
    ## handle dottet name path
    path = namepath.split(".")
    if len(path) > 1:
      if path[0] in self._items:
        schema = self._items[path[0]]
      else:
        schema = _Schema(self, path[0])
        self._items[path[0]] = schema
      if not isinstance(schema, _Schema):
        raise AttributeError(
          "'{}' assigned as schema group, but is alread declared to '{}'".
          format(path[0], self._items[path[0]].vdefault))
      schema(".".join(path[1:]), vdefault) # sub declaration
    else:
      item = _Item(self, path[0], vdefault)
      self._items[path[0]] = item
      
  @property
  def items(self):
    for key in self._items:
      yield self._items[key]
    
  @property
  def is_schema(self):
    return True
    
##############################################################################

def fill(s):
  s("test", 1001)
  #s("test.nowork",1)
  s("group.test", 2002)
  s("group.joo", "jeejee")
  s("group.group.name","dvalue")

def run1():
  s = _Schema()
  fill(s)
  def walk(schema, indent):
    for item in schema.items:
      print("  " * indent, item.name)
      if item.is_schema:
        indent += 1
        walk(item, indent) 
        indent -= 1     
  walk(s, 0)

if __name__ == "__main__":
  logging.basicConfig(format=LOGFORMAT, level=logging.DEBUG)
  run1()

