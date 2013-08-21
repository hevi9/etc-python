
def func(a1:int) -> int:
  pass

def func2(a1:int = 10) -> int:
  pass

class Something: pass

def func3(a1: Something):
  print(type(a1))
  
class Something: 
  pass

func3(Something())