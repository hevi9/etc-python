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
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

##############################################################################
## 

##############################################################################
## entry

def main():
  logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__": main()  

