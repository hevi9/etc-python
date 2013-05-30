import collections # http://docs.python.org/3.3/library/collections.html

class DictWrap(collections.UserDict):
  
  def __init__(self,*args,**kwds):
    super().__init__(*args,**kwds)
    
  def __getattr__(self,key):
    if key == "data":
      return getattr(super(),key)
    else:
      return self.data[key]
    
  def __setattr__(self,key,value):
    print("__setattr__(self,{key},{value})".format(**locals()))
    if key == "data":
      setattr(super(),key,value)
    else:
      self.data[key] = value
    
##

d = {"key1": 1001}

dw = DictWrap(d)

print(dw["key1"]) 

for k,v in dw.items():
  print(k,"=",v)

print(dw.key1)
