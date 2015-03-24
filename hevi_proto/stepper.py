#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
"""
stepper - Console user interface to report program operation process
====================================================================
"""

class _Step:
  
  def result(self):
    pass
  
  def error(self):
    pass

# sub steps

class _Stepper:
  
  def step(self, txt):
    step = _Step(txt)
    return step;
  
  def long_step(self,txt):
    return step;
  
  def result(self):
    pass
  
  def error(self):
    pass
