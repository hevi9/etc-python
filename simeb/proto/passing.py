#!/usr/bin/env python3
## -*- coding: utf-8 -*-

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import json
import asyncio
import functools

class Bus():
  
  def __init__(self):
    self._msgs = dict()
    
  def register(self, fn):
    D("register %s", fn.__name__)
    self._msgs[fn.__name__] = fn
    
  def invoke(self, msg, *params):
    fn = self._msgs[msg]
    D("invoke %s", fn.__name__)
    fn(*params)
    
  def encode(self, msg, *params):
    D("encode %s%s", msg, params)
    msg_obj = [msg]
    msg_obj.extend(params)
    data = json.dumps(msg_obj)
    self.decode(data)
    
  def decode(self, data):
    D("decode %s", data)
    obj = json.loads(data)
    msg = obj.pop(0)
    params = obj
    self.invoke(msg, *params)
    
  def __getattr__(self, name):
    D("__getattr__ %s", name)
    return functools.partial(self.encode, name)
    

bus = Bus()

def msg(param):
  D("receive msg %s", param)

def send():
  param = "B"
  D("send msg %s", param);
  #msg(param)
  #bus.invoke("msg", param)
  bus.msg(param)
  

def main():
  logging.basicConfig(level=logging.DEBUG)
  bus.register(msg)
  send()
  D("done.")


if __name__ == "__main__":
  main()
  