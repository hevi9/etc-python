
def f1(*args):
  print(*args)

def f2(*args):
  print(args)

def f3(*args):
  l = (4,5,6)
  new = args + l
  print(new)

def f4(*args):
  l = (4,5,6)
  new = args + l
  print(*new)

f1(1,2,3)
f2(1,2,3)
f3(1,2,3)
f4(1,2,3)