#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1

##############################################################################
## Code

from hevi_misc.hevi_code_to_page import *

class cfg1:
  in_root = ["/home/hevi/wrk/learning_python3"]
  in_match = ["*.py"]
  out_html = "/home/hevi/public_html/code/learning_python3.html"

class cfg2:
  in_root = ["/home/hevi/wrk/learning"]
  in_match = ["*.py","*.html"]
  out_html = "/home/hevi/public_html/code/learning.html"

class cfg3:
  in_root = ["/home/hevi/wrk/learning"]
  in_match = ["*.c","*.h","*.cc"]
  out_html = "/home/hevi/public_html/code/learning_c.html"

class cfg4:
  in_root = ["/home/hevi/wrk/hevi_util"]
  in_match = ["*.txt","*.py"]
  out_html = "/home/hevi/public_html/code/hevi_util.html"

class cfg5:
  in_root = ["/home/hevi/wrk/hevi_misc"]
  in_match = ["*.txt","*.py"]
  out_html = "/home/hevi/public_html/code/hevi_misc.html"

class cfg6:
  in_root = ["/home/hevi/wrk/comdl"]
  in_match = ["*.txt","*.py"]
  out_html = "/home/hevi/public_html/code/comdl.html"


def run():
  ui = UI()
  tasks = [FormatTask(cfg1,ui),
           FormatTask(cfg2,ui),
           FormatTask(cfg3,ui),
           FormatTask(cfg4,ui),
           FormatTask(cfg5,ui),
           FormatTask(cfg6,ui)                      
           ]
  for task in tasks:
    task.begin()
  for task in tasks:
    task.run()
  for task in tasks:
    task.end()

##############################################################################
## Running
  
if __name__ == "__main__":
  run()
  