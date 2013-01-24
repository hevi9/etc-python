#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
""" """

from distutils.core import setup
import os
j = os.path.join

scripts = [j("bin",f) for f in os.listdir("bin")]

setup(
  name='hevi_proto',
  version='0.1',
  description='Prototype ideas',
  author='Petri Heinilä',
  url='http://github.com/hevi9/hevi_proto',
  packages=['hevi_proto'],
  scripts = scripts,
  package_data = {'hevi_proto': ["*"]}
)