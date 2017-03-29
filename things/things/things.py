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
import fnmatch
from .thingx import Thing, make_thing


OPS = "==>"  # operation sign
TGS = "[]"  # thing sign


ARGS = argparse.ArgumentParser()
ARGS.add_argument("title", nargs="*",
                  help="""Thing title text, arguments are concatenated into same
                  title text, extra spaces are stripped""")
ARGS.add_argument("-d", "--debug", action="store_true",
                  help="set Debugging/Development mode on")
ARGS.add_argument("-r", "--remove", action="store_true",
                  help="Remove thing by title")
ARGS.add_argument("-c", "--config", action="store_true",
                  help="Configure, TODO")
ARGS.add_argument("-n", "--new", action="store_true",
                  help="create New thing")
ARGS.add_argument("-u", "--uuid", action="store_true",
                  help="specify thing by UUID, TODO")
ARGS.add_argument("-s", "--show", action="store_true",
                  help="show a thing, TODO")


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


def thing_new(things, title):
    D("Create new thing")
    cursor = things.find({"title": title})
    if cursor.count() == 0:
      print(OPS, "new thing '%s'" % title)
      thing = make_thing(title)
      thing.mongo_insert(things)
    else:
      print(OPS, "thing '%s' exists already, no thing need to be done" % title)


def thing_list(things, match=""):     
  match = ".*" if match == "" else "^.*" + match + ".*$"
  D("Listing things for match '%s'", match) 
  for data in things.find({"title": {"$regex": match}}):
    thing = Thing()
    thing.update(data)
    print("[]",thing.title)  


def thing_show(things, title):
  D("show a thing '%s'" % title)
  data = things.find_one({"title":title})
  if data:
    thing = Thing()
    thing.update(data)
    print(TGS,thing.title)
    print("  ctime = ", thing.ctime)
    print("  uuid  = ", thing.uuid)
  else:
    print(OPS, "thing '%s' does not exist" % title)


def setup_logging(args):
  logging.basicConfig()
  if args.debug:
    logging.getLogger().setLevel(logging.DEBUG)
  

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
    
  if args.new:
    thing_new(things, title)
    sys.exit(0)
    
  if args.show:
    thing_show(things, title)
    sys.exit(0)  

  thing_list(things, title)  
  sys.exit(0)


if __name__ == "__main__":
  main()

