
import logging
log = logging.getLogger(__name__)
D = log.debug
import json
import inspect

##############################################################################
    
class Ctrl:

  def __init__(self):
    D("__init__")

  def __getattr__(self, key):
    D("__getattr__ %s", key)
    try:
      return object.__getattribute__(self, key)
    except AttributeError:
      self.__dict__[key] = Ctrl() # schema check
      return object.__getattribute__(self, key)

  def __setattr__(self, key, value):
    D("__setattr__ %s=%s", key, value)
    self.__dict__[key] = value
  
  def __iter__(self):
    return iter(self.__dict__)

  def __getitem__(self, key):
    return self.__dict__[key]

##############################################################################

def fill(ctrl):
  ctrl.test = 1001
  ctrl.args.debug = True
  ctrl.app.flag = 10
    
def enlist(ctrl):
  for name in ctrl:
    D("member %s=%s", name, ctrl[name])
    if isinstance(ctrl[name], Ctrl):
      enlist(ctrl[name])

def run4():
  ctrl = Ctrl()
  fill(ctrl)
  enlist(ctrl)

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run4()

