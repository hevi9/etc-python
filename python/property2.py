# check readonly

class A:
  
  def __init__(self):
    self._readonly = 1
    
  @property 
  def readonly(self): return self._readonly
  
  
a = A()
print(a.readonly)
a.readonly = 2