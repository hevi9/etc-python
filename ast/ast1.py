import ast
from pprint import pprint
from astpp import dump
#from ast import dump

code = """
x = 1
"""

code = """
x, y = 1, 1
"""

code = """
@deco
def fn(a, *, b=100):
  pass
"""

code = """
class Klass:
  def fn1():
    pass
  def fn2(a, *, b=100):
    pass
"""



def run():
  tree = ast.parse(code)
  print(dump(tree))
  
run()


