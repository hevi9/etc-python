#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Petri Heinilä, LGPL 2.1

import sys       # http://docs.python.org/py3k/library/sys.html
import argparse  # http://docs.python.org/py3k/library/argparse.html
import logging   # http://docs.python.org/py3k/library/logging.html
from _datetime import datetime
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error
import time
import datetime
import uuid as muuid
from pymongo import MongoClient

OPS = "==>"  # operation sign
TGS = "[]"  # thing sign


class Thing:
  
  def debug(self):
    D("title='%s':%s",self.title, type(self.title))
    D("ctime='%s':%s", self.ctime, type(self.ctime))
    D("uuid='%s':%s", self.uuid, type(self.uuid))

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


ARGS = argparse.ArgumentParser()
ARGS.add_argument("title", nargs="*",
                  help="Positional arguments")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set debugging on")
ARGS.add_argument("-r", "--remove", action="store_true",
                  help="Remove thing by title")

def setup_logging(args):
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)

def thing_remove(things, title):
  D("thing_remove %s '%s'", things, title)
  cursor = things.find({"title": title})
  if cursor.count() == 1:
    data = cursor[0]
    things.remove({"title":title})
    print(OPS, "'%s' removed" % title)
  elif cursor.count() == 0:
    print(OPS,"no thing '%s' found to remove" % title)
  else: # more than 1
    print(OPS,"found %d things '%s', cannot remove" % (cursor.count(), title))

def main():
  args = ARGS.parse_args()
  setup_logging(args)
  
  title = " ".join(args.title).strip()
  
  mongo = MongoClient()
  db = mongo.thingsdb
  things = db.things
  
  if args.remove:
    thing_remove(things, title)
    sys.exit(0)
  
  if title.strip() == "": 
    D("Listing things")
    for data in things.find():
      thing = Thing()
      thing.update(data)
      print("[]",thing.title)
  else:
    D("Create new if") 
    cursor = things.find({"title": title})
    if cursor.count() == 0:
      D("no thing in db, making new")
      print(OPS, "new thing '%s'" % title)
      thing = make_thing(title)
      thing.mongo_insert(things)
    else:
      D("thing in db")
      thing = Thing()
      thing.update(cursor[0])    
      cursor.close()
    thing.debug()
  
  
  sys.exit(0)


if __name__ == "__main__":
  main()

