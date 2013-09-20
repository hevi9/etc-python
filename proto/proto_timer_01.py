#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2009 Petri Heinilä, License LGPL 2.1
__tags__    = "proto"
__version__ = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__ = "$Release$"
__docformat__ = "epytext"
"""
Scheduler
Dispatcher
Task

by time
by I/O
by queue

"""

##############################################################################
## Uses

import sys
import os
import logging
log = logging.getLogger(__name__)
import unittest
import time

##############################################################################
## 

class Timer(object):
  """
  Timer(+10s,on_timeout,*args,**kwds)
  Timer(+every10s,on_timeout,*args,**kwds)
  Timer(=fixedtime,on_timeout,*args,**kwds)
  state:
    idle
    waiting    
  """
  def __init__(self):
    pass

  def start(self):
    pass
  
  def cancel(self):
    pass
  
  def _fire(self):
    pass

##############################################################################
## 

class TimeDispacther(object):
  """
  """
  def __init__(self):
    pass
  
  def timer_next(self,offset,on_timeout,*args,**kwds):
    pass
  
  def timer_interval(self,interval,on_timeout,*args,**kwds):
    pass
  
  def timer_time(self,ftime,on_timeout,*args,**kwds):
    pass
  
  def step(self):
    """
    Execute one timeout function. 
    """
    pass
    
  def remove(self,timer):
    pass

##############################################################################
## Proto usage

class test_Proto(unittest.TestCase):
  
  def test_usage(self):
    """ usage """
    print type(time.time())
    print time.time()
    print time.localtime(time.time())


##############################################################################
## This file activation  
  
if __name__ == '__main__':
  logging.basicConfig()
  rootlog = logging.getLogger()    
  rootlog.setLevel(logging.DEBUG)
  unittest.main()
