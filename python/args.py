
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

def repeat (function, params, times):
    for calls in range (times):
        function (*params)

def foo (a, b):
    print ('{} are {}'.format (a, b) )

repeat (foo, ['roses', 'red'], 4)
repeat (foo, ['violets', 'blue'], 4)

def test(fn,*args):
  print(args)
  fn(*args)
  
test(foo,1,2)
  
def test2(fn,*args,**kwds):
  fn(1000,*args, **kwds)
  
test2(foo,2)
