#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2012 Petri Heinilä, License LGPL 2.1

##############################################################################
## Code

from hevi_misc.hevi_code_to_page import *

def run():
  ui = CmdUI()
  args = ui.parse()
  task = FormatTask(args,ui)
  task.begin()
  task.run()
  task.end()

##############################################################################
## Running
  
if __name__ == "__main__":
  run()
  