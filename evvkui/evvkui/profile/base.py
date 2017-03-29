


class Engine:
  """ Concrete implementation of toolkit, widgets and policies. """

class Widget:
  """ User interface component. """
  
  @property
  def title(self):
    """
    Type is str. Is localized by engine. 
    """
    
  @property
  def when_default(self):
    """ Callback point when default event occurs on widget. 
    calls on_default function. """
  
class Mono(Widget):
  """ Widget containint on child widget. 
  needed ? """
  
class Control(Widget):
  """ Widget reresenting some value.
  Does not have childs.  
  """
  
class Frame(Widget):
  """ Widget containing multiple child widgets and
  allocating and ordering them in some way. """
  
class Window(Frame):
  """ User interaction point to application. """
