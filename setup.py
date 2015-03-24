#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
""" """

from setuptools import setup
from hevi_util.setups import package_data, console_scripts

pkg = "hevi_proto"

setup(
  name='hevi_proto',
  version='0.1.1',
  description='Prototype ideas',
  author='Petri Heinila',
  url='http://github.com/hevi9/hevi_proto',
  packages=['hevi_proto'],
  package_data = {'hevi_proto': package_data(pkg)},
  entry_points={
    'console_scripts': console_scripts(pkg)
  }
)