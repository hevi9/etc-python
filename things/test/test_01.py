#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Petri Heinilä, LGPL 2.1

import logging # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import pytest

import sys
sys.path.append("..")

from things.thingx import Thing


def test_01():
  """ Testing 01 """  
  D("test_01 here")
  Thing({})


if __name__ == "__main__":
  pytest.main()
