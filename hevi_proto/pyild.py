#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
"""
pyild - build management system
===============================

pyild - python build system (proto)


Goal is to collect software building scripts into
central manageable place.

Sample
------

start
::
  b('''
  git clone git://anongit.freedesktop.org/wayland/wayland
  cd wayland
  ./autogen.sh --prefix=$WLD
  make
  make install
  ''')

cd wayland is problematic

Proto: Automated file management system (pymake)
************************************************

Motivation
==========

Why use other tool than (gnu)make or cook ?

  * being able to to have programming capability as much needed in rules
    execution
  * total control: tracking every phase

Operation
=========

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

Syntax
======

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

