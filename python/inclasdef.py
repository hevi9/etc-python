import inspect

def wrap(value):
  print("wrap",value)
  rec = inspect.stack()[1]
  print(rec)
  frame = rec[0]
  print(frame.f_code.co_name)
  return value

class control_base:
  
  def __init__(self):
    print("control_base init")
    print(dir(self))

class control(control_base):
  
  thing = wrap(100)
  
  class sub1:
    
    var = 200

  class sub2:
    
    var = 200



control = control()

print(control.thing)


