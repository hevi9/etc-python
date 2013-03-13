print("------------------------------------------------------------")

def deco1(obj):
  print("deco1",obj)
  return obj
  
@deco1
def fn1():
  print("fn1")
  
@deco1
class cls1():

  @deco1
  def met1(self):
    print("met1")

print("------------------------------------------------------------")

def deco2(obj):
  print("deco2",obj)
  return obj
  
@deco1
@deco2
def fn2():
  print("fn2")
  
@deco1
@deco2
class cls2():

  @deco1
  @deco2
  def met2(self):
    print("met2")

print("------------------------------------------------------------")

def deco3(arg1,arg2):
  print("deco3",arg1,arg2)
  def subdeco(obj):
    print("deco3.subdeco",obj)
    return obj
  return subdeco

@deco3("a","b")
def fn3():
  print("fn3")

fn3()
  