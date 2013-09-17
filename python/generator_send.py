
# code::

def g1():
  x = yield "yield 1"
  print(x)
  
# the point is the::
#   
#   x = yield "yield 1"
#
# calling with send::
  
g = g1()
r = g.send(None)
print(r)
r = g.send("send 1")
print(r)