import logging
log = logging.getLogger(__name__)
D = log.debug

logging.basicConfig(level=logging.DEBUG)

class Prop:

  def __init__(self, default=None):
    D("Prop.__init__")
    self.default = default
        
  def __get__(self, instance, owner):
    D("Prop.__get__ %s %s",instance, owner)
    if instance is None:
      return self        
    return self.default
  
  def __set__(self, instance, value):
    D("Prop.__set__ %s %s", instance, value)        
    self.default = value
  
class Klass:
  prop = Prop(19)
      
def run1():
  klass = Klass()
  D(klass.prop)
  klass.prop = 12

class Klass2:
  
  def __init__(self):
    self.prop = Prop(16)
    
def run2():
  klass = Klass()
  klass.prop = 99
  D(klass.prop)
  D(Klass2.prop)


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  run2()
