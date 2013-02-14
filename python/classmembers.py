

class A:
  debug = False
  
  def do(self):
    print("class debug = {}".format(self.debug))
    
a1 = A()
a1.do()

a2 = A()
print(a2.__dict__)
a2.debug = True
print(A.__dict__)
print(a2.__dict__)
a2.do()
a1.do()
print(A.debug)