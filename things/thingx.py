#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Petri Heinilä, LGPL 2.1

import logging
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error
import datetime
import uuid


class Thing:
    
  __slots__ = ("type", "title", "ctime", "uuid")
  __types__ = {
    "type": str,
    "title": str,
    "ctime": datetime.datetime,
    "uuid": uuid.UUID
  }
  
  def __init__(self, data):
    try:
      self.type = data["type"]
    except KeyError:
      self.type = "thing"
    self.title = data["title"]
    self.ctime = data["ctime"]
    self.uuid = data["uuid"]
  
  def debug(self):
    for field in self.__slots__:
      value = getattr(self, files)
      D("%s='%s':%s", field, value, type(value))

  def mongo_insert(self, col):
    col.insert({
      "title": self.title,
      "ctime": self.ctime,
      "uuid": self.uuid      
    })

  def update(self, data):
    self.title = data["title"]
    self.ctime = data["ctime"]
    self.uuid = data["uuid"]


def make_thing(title):
  """ Function does that. """
  thing = Thing()
  thing.title = title
  thing.ctime = datetime.datetime.utcnow()
  thing.uuid = muuid.uuid4()
  return thing  

