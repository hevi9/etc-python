import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Left:

  def __init__(self):
    log.debug("Left.__init__()")
    
class Right:

  def __init__(self):
    log.debug("Right.__init__()")
  
## with plain super
    
class Inherited(Left, Right):

  def __init__(self):
    super().__init__()
    log.debug("Inherited.__init__()")
    
obj = Inherited()

## with plain super and named call
    
class Inherited2(Left, Right):

  def __init__(self):
    super().__init__()
    super(Right,self).__init__()
    log.debug("Inherited2.__init__()")
    
obj2 = Inherited2()
  