import ast
from pprint import pprint
from astpp import dump
import logging
log = logging.getLogger(__name__)

code = """
from joo import jee

jrr = joo = 100

class Klass:
  def fn1():
    pass
  def fn2(a, *, b=100) -> 1 + 1:
    2 + 2
"""

SKIP = [
  "Add",
  "Num",
  "BinOp",
  "Pass",
  "Module",
  "Assign",
  "Store",
  "Expr",
  "arguments"
]

class Visitor(ast.NodeVisitor):

  def __init__(self, add_name_cb):
    self._add_name_cb = add_name_cb
  
  def generic_visit(self, node):
    not_handled(node)
    super().generic_visit(node)

  def visit_arg(self, node):
    self._add_name_cb(node.arg)
    if node.annotation:
      not_handled(node.annotation)
    super().generic_visit(node)

  def visit_alias(self, node):
    self._add_name_cb(node.name)
    super().generic_visit(node)
    
  def visit_ImportFrom(self, node):
    self._add_name_cb(node.module)
    super().generic_visit(node)
    
  def visit_Name(self, node):
    self._add_name_cb(node.id)
    super().generic_visit(node)
    
  def visit_ClassDef(self, node):
    self._add_name_cb(node.name)
    super().generic_visit(node)

  def visit_FunctionDef(self, node):
    self._add_name_cb(node.name)
    super().generic_visit(node)

def not_handled(obj):
  if isinstance(obj, ast.AST):
    name = obj.__class__.__name__
    if name not in SKIP:
      log.warn("not handled %s %s", name , obj._fields)
  else:
    log.warn("not handled %s", obj)


class Stats:

  def __init__(self):
    self.names = dict()

  def add_name(self, name):
    #log.info("name=%s", name)
    self.names[name] = self.names.setdefault(name, 0) + 1

  def report(self):
    print(" ".join(["%s(%s)" % (x,self.names[x]) for x in sorted(self.names)]))

def run():
  logging.basicConfig(level=logging.DEBUG)
  tree = ast.parse(code)
  s = Stats()
  v = Visitor(s.add_name)
  v.visit(tree)
  s.report()
  #print(dump(tree))
  
  
run()


