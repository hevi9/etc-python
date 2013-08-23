import collections

class Set1(collections.MutableSet):
  
  def __init__(self,ctx):
    super().__init__()
    self.data = set()
    self.ctx = ctx
    
  def __contains__(self, x): return x in self.data

  def add(self, value):
    pass

  def discard(self, value):
    pass
  
  def __iter__(self):
    pass
  
  def __len__(self):
    pass

class Set2(set):

  def __init__(self,ctx):
    super().__init__()
    self.ctx = ctx

  def add(self, value):
    super().add(value)
    ctx.on_add(value)

  def discard(self, value):
    super().discard(value)
    ctx.on_discard(value)

class Ctx:
  
  def on_add(self,value):
    print("on_add",value)

  def on_discard(self,value):
    print("on_discard",value)


ctx = Ctx()

set1 = Set1(ctx)

set2 = Set2(ctx)
set2.add("A")
set2.add("B")
print("set2",set2)
set2.discard("B")
print("set2",set2)

