#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
""" """

from setuptools import setup
import os
j = os.path.join
from etc.util import * 

pkg = "hevi_proto"

def isdata(f):
  if f == "__pycache__": return False
  if f == ".gitignore": return False
  return True

datas = [f for f in os.listdir(pkg) if isdata(f)]

def ismain(f):
  if os.path.splitext(f)[1] != ".py": return False
  m = import_file(f)
  if not hasattr(m,"main"): return False
  return callable(getattr(m,"main"))

mains = [j(pkg,f) for f in os.listdir(pkg) if ismain(j(pkg,f))]

console_scripts = list()

for mainfile in mains:
  cmd = os.path.basename(os.path.splitext(mainfile)[0])
  mod = module_name(mainfile)
  console_scripts.append(
    "{} = {}:main".format(cmd,mod))

setup(
  name='hevi_proto',
  version='0.1.1',
  description='Prototype ideas',
  author='Petri Heinila',
  url='http://github.com/hevi9/hevi_proto',
  packages=['hevi_proto'],
  package_data = {'hevi_proto': datas},
  entry_points={
    'console_scripts': console_scripts
  }
)