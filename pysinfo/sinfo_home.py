#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from .data import sinfo_apply 
import os 

path = os.environ["HOME"]

def get_stats():
  nfiles = 0
  for dir, dirs, files in os.walk(path):
    nfiles += len(files)
  return nfiles  

nfiles = get_stats()

data = {
  "path": path
  
}

sinfo_apply("home", data)