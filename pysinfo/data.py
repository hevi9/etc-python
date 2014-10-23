#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

import asyncio

sinfo = dict()

update_coros = list()

def sinfo_apply(section, data, update_coro):
  global sinfo
  sinfo[section] = data
  update_coros.append(update_coro)
  
def sinfo_update():
  for coro in update_coros:
    asyncio.async(coro())
  