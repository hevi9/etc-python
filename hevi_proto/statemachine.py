"""
State pattern implementation in pyython
=======================================
"""

import functools

class Context:

  def __init__(self):
    self.__state = None

  @property
  def state(self):
    return self.__state
  
  @state.setter
  def state(self, newstate):
    if self.__state is None:
      log.debug("Initia state ({})".format(newstate.__name__))
    else:
      log.debug("({}) => ({})".format(self.__state.__name__,newstate.__name__))
    self.__state = newstate

  def __getattr__(self,attr):
    return functools.partial(getattr(self.state,attr),self)

## example

class Door(Context):
  
  def __init__(self):
    super().__init__()
    self.state = self.CLOSED
      
  ## states
  
  class DEFAULT:
  
    def open(self):
      print("already open")
      
    def close(self):
      print("already closed")
  
  class OPEN(DEFAULT):
    
    def close(self):
      print("closing door")
      self.state = self.CLOSED
    
  class CLOSED(DEFAULT):
    
    def open(self):
      print("opening door")
      self.state = self.OPEN
    
## example run

def main1():
  door = Door()
  door.open()
  door.close()
  door.close()

## entry

if __name__ == "__main__":
  import logging
  global log
  log = logging.getLogger(__name__)
  logging.basicConfig(level=logging.DEBUG)
  main1()
  
"""

class Door:

  @state("CLOSED","OPEN")
  def open():
    closing action

  @state("CLOSED","CLOSED")
  def close():
    closing action

  @state("OPEN","CLOSED")
  def close():
    closing action

  @state("OPEN","OPEN")
  def open():
    closing action

  # vs
  
  class OPEN:
  
    def open():
      pass
      
    def close();
      pass
      



"""

    