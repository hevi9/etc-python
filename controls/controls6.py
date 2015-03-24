
import logging
from collections import deque
log = logging.getLogger(__name__)
D = log.debug

##############################################################################

class _Base:
  
  def __init__(self, schema=None, name=None):
    if name is not None:
      assert not name.startswith("_")
    self._schema = schema
    self._name = name

  @property
  def name(self):    
    return self._name if self._name is not None else "<ROOT>"
  
  @property
  def schema(self):
    return self._schema
  
  @property
  def root(self):
    return self if self._schema is None else self.root    
  

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
    D("new _Schema '%s'", self.name)
    
  def __call__(self, namepath, vdefault):
    D("%s <= %s=%s", self.name, namepath, vdefault)
    ## handle dottet name path
    path = namepath.split(".")
    if len(path) > 1:
      schema = self._items.setdefault(path[0], _Schema(self, path[0])) # ??? 
      if not isinstance(schema, _Schema):
        raise AttributeError(
          "'{}' assigned as schema group, but is alread declared to '{}'".
          format(path[0], self._items[path[0]].vdefault))
      schema(".".join(path[1:]), vdefault) # sub declaration
    else:
      item = _Item(self, path[0], vdefault)
      self._items[path[0]] = item

##############################################################################

def fill(s):
  s("test", 1001)
  s("group.test", 2002)
  s("group.joo", "jeejee")

def run1():
  s = _Schema()
  fill(s)

if __name__ == "__main__":
  FORMAT = "[%(levelname)s|%(filename)s:%(lineno)s|%(funcName)s] %(message)s"
  logging.basicConfig(format=FORMAT, level=logging.DEBUG)
  run1()

