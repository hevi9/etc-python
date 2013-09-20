#!/usr/bin/env python
## -*- coding: utf-8 -*-
## Copyright (C) 2008 Petri Heinilä, License LGPL 2.1
__tags__      = "module"
__version__   = "$Id: process.py 3202 2008-10-24 10:02:11Z hevi $"
__release__   = "$Release$"
__docformat__ = "epytext"
"""
"""

import logging
log = logging.getLogger(__name__)
import hevi_util.main as hum
import hevi_util.task as hut


def task_kwds_run():
  log.debug("task_kwds_run:")  
  def aRun():
    log.debug("task_kwds_run - aRun")  
  task = hut.Task(run=aRun)
  task.start()

def task_kwds_call_run():
  log.debug("task_kwds_call_run:")  
  def aRun():
    log.debug("task_kwds_call_run - aRun")  
  task = hut.Task(run=aRun)
  task()



def run():
  task_kwds_run()
  task_kwds_call_run()

  
if __name__ == "__main__":
  main = hum.Main(run=run,debug=True)
  main.start()
  