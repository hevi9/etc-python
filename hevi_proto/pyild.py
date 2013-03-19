#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1

"""
pyild - file manipulation system
================================

Goal is to manipulate files for building target results. Pyild is
partial replacement of the make tool. In contrast to make pyild provides:
1) programmability with python language 2) OS independency support 3)
execution tracking and visualization functionalities 4) holistic 
control of execution.

Thins from make that are definetly kept same: 1) current work directory
based execution 2) directory based rule, task and recource definition
3) agnostic rules, no in-build magic, but explicit rule and resoure 
libraries (or modules) 4) dependency grapth based execution.  

Related systems: 1) make and it's variants 3) cook 3) python paver_ 
4) python waf_ 5) fabric_ 6) shovel_ 7) python buildout from zope.

.. _paver http://paver.github.com/paver/
.. _waf http://code.google.com/p/waf/
.. _fabric https://fabric.readthedocs.org/en/latest/
.. _shovel https://github.com/seomoz/shovel
.. _buildout http://www.buildout.org/

Operation
---------

Basic:

1. Define and select resources (libraries and external programs)

2. Discover files and construct dependency graph

3. Execute graph by depth-first traversal with resources

Resource tracking:

1. Define and select resources (libraries and external programs)

2. List used resource: used external programs in this host, defined
   external program possibilities, used defined python pymake library
   resources 

Dependency graph tracking:

Execution tracking:


Samples
-------

start::

  b('''
  git clone git://anongit.freedesktop.org/wayland/wayland
  cd wayland
  ./autogen.sh --prefix=$WLD
  make
  make install
  ''')

cd wayland is problematic

sample::

  @rule("target.txt","source1.txt","source2.txt")
  def dummy1(ctx):
    sh.cat(ctx.srcs,ctx.trgs[0])

make comparison::

  target.txt: source1.txt source2.txt
    cat $@ > $$

"""

##############################################################################
## Uses & module setup

import logging # http://docs.python.org/py3k/library/logging.html
import sys # http://docs.python.org/py3k/library/sys.html
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
from py._builtin import execfile


################################################################(##############
## execution dependency model

class CycleError(Exception): pass 

class Space:
  
  def __init__(self):
    self._targets = dict()
    self._default = None
    
  @property 
  def default(self):
    return self._default
    
  def target(self,value):
    target = self._targets.setdefault(value, Target(value))
    if self._default is None:
      self._default = target
    return target
  
  def execute(self, target):
    if isinstance(target, str):
      target = self._targets[target]
    for depend in target.depends:
      if depend.source is not None:
        self.execute(depend.source)
    for depend in target.depends:
      depend.func()
          
  def has_cycle(self, depend):
    # trivial
    if depend.target == depend.source:
      return True
    return False
      
space = Space()

globals = dict()

class Target:
  
  def __init__(self, value, space=space):
    self._value = value
    self._space = space
    self._depends = list() # Depend

  def __str__(self):
    return self._value

  @property
  def value(self):
    return self._value
    
  @property
  def depends(self):
    return self._depends

  def add_depend(self,depend):
    if space.has_cycle(depend):
      raise CycleError("Dependency cycle from {} to {}".format(
        depend.target,depend.source))
    self._depends.append(depend)
  
class Depend:
  
  def __init__(self, func, target, source=None):
    self._func = func
    self._target = target
    self._source = source
    self._doc = func.__doc__
    
  @property
  def target(self):
    return self._target
  
  @property
  def source(self):
    return self._source
  
  @property
  def func(self):
    return self._func
  
##############################################################################
## decorator

def task(arg1):
  if callable(arg1): # as @task
    log.debug("task({})".format(arg1))
    func = arg1
    target = space.target(func.__name__)
    target.add_depend(Depend(func,target))
    return arg1
  else: # as task(args ..)
    log.debug("task({})".format(arg1))
    def warp(func):
      log.debug("task.wrap({})".format(func))
      target = space.target(func.__name__)
      source = space.target(arg1)
      target.add_depend(Depend(func,target,source))
      return func
    return warp

##############################################################################
## entry

def main():
  logging.basicConfig(level=logging.DEBUG)
  execfile("pyildfile", globals)
  if len(sys.argv) > 1:
    for target in sys.argv:
      space.execute(target)
  else:
    space.execute(str(space.default))

if __name__ == "__main__": main()  

