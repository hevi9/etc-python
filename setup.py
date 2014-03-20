#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from setuptools import setup, find_packages
from hevi_lib.setups import package_data, console_scripts
from hevi_lib.modules import inject

inject("INFO")

setup(
  #install_requires=['setuptools'], # -U seems to re-force setuptools installation
  name=name,
  version=version,
  description=title,
  author=author,
  url=url,
  packages = find_packages(),
  package_data = {name: package_data(name) },
  entry_points={
    'console_scripts': console_scripts(name)
  },
  license = license
)