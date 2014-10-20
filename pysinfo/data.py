#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

sinfo = dict()

def sinfo_apply(section, data):
  global sinfo
  sinfo[section] = data
  
  