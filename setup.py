#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from setuptools import setup, find_packages

info = dict()
with open("INFO") as f:
  exec(f.read(),info)

setup(
  name=info["name"],
  version=info["version"],
  description=info["title"],
  author=info["author"],
  url=info["url"],
  license = info["license"],
  packages = find_packages(),
  entry_points={
    "console_scripts": [
      "pysinfo=pysinfo.pysinfo:main"
    ]
  }
)