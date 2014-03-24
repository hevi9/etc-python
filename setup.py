#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from setuptools import setup, find_packages

with open("INFO") as fo:
  exec(fo.read())

setup(
  #install_requires=['setuptools'], # -U seems to re-force setuptools installation
  name=name,
  version=version,
  description=title,
  author=author,
  url=url,
  packages = find_packages(),
  license = license
)