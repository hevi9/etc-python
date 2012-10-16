""" """

class B:
  
  def __iter__(self):
    pass
    
  def __getitem__(self,key):
    return getattr(self,key)

  @property
  def data1(self):
    return "VALUE1"

b = B()

print(vars(b))

#for key in b:
#  print(key,b[key])