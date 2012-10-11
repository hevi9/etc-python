
def call(f):
  f()

def top():
  a = "top"
  def sub1():
    a = "sub1"
    print("sub1()")
  def sub2():
    a = "sub2"
    print("sub2()")    
  call(sub1)
  print(a)
  
top()

class Klass:
  def top(self):
    self.a = "ktop"
    def sub1():
      self.a = "ksub1"
      print("sub1()")
    def sub2():
      self.a = "ksub2"
      print("sub2()")    
    call(sub2)
    print(self.a)

print("klass")
k = Klass()
k.top()