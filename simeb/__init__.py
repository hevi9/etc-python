#!/usr/bin/env python3.4
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

PORT = 45678

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
I = log.info
E = log.error
import json
import asyncio
import functools
import sys
import errno

##############################################################################


class Broker:

  def __init__(self):
    self._links = set()
    self._buses = dict()
    self._server = None
    asyncio.Task(self._start())

  # greedy server strategy
  @asyncio.coroutine
  def _start(self):
    D("Broker.start")
    try:
      self._server = yield from asyncio.start_server(self.client_connected_cb,
                                                     "localhost", PORT)
    except OSError as ex:
      if ex.errno != errno.EADDRINUSE:
        print(str(ex))
        sys.exit(2)
      else:
        self.link()

  def client_connected_cb(self, reader, writer):
    D("client_connected_cb from %s",
      writer.transport.get_extra_info("peername"))
    self._links.add(Link(self, reader, writer))

  def close(self):
    self._server.close()

  @asyncio.coroutine
  def link(self, host="localhost", port=PORT):
    D("link %s %s", host, port)
    reader, writer = yield from asyncio.open_connection(host, port)
    self._links.add(Link(self, reader, writer))

  def writeline(self, line):
    D("SEND to %i links", len(self._links))
    for link in self._links:
      link.writeline(line)

  def dispatch(self, line):
    obj = json.loads(line)
    msg = obj.pop(0)
    params = obj
    for bus in self._buses.values():
      bus.invoke(msg, *params)

  def bus(self, name="SYS"):
    bus = self._buses.setdefault(name, Bus(self, name))
    return bus

##############################################################################


class Bus:

  def __init__(self, broker2, name="SYS"):
    self._name = name
    self._broker = broker2
    self._msgs = dict()

  def register(self, fn):
    D("register %s", fn.__name__)
    self._msgs[fn.__name__] = fn

  def invoke(self, msg, *params):
    try:
      fn = self._msgs[msg]
    except KeyError:
      D("no msg '%s' in bus '%s'", msg, self._name)
      return
    D("invoke %s", fn.__name__)
    fn(*params)

  def encode(self, msg, *params):
    D("encode %s%s", msg, params)
    msg_obj = [msg]
    msg_obj.extend(params)
    line = json.dumps(msg_obj)
    self._broker.writeline(line)

  def __getattr__(self, name):
    D("__getattr__ %s", name)
    return functools.partial(self.encode, name)

##############################################################################


class Link:

  def __init__(self, broker2, reader, writer):
    self._broker = broker2
    self._reader = reader
    self._writer = writer
    asyncio.Task(self._readline())
    D("Link()")

  @asyncio.coroutine
  def _readline(self):
    while True:
      line = yield from self._reader.readline()
      if not line:
        break
      line = line.decode()
      D("_readline %s", line)
      self._broker.dispatch(line)

  def writeline(self, line):
    D("writeline %s", line)
    line = line + "\n"
    data = line.encode()
    self._writer.write(data)


##############################################################################
## process wide singleton

__broker = None


def broker():
  global __broker
  if not __broker:
    __broker = Broker()
  return __broker

##############################################################################


def make_link(host="localhost", port=PORT):
  asyncio.Task(broker().link(host, port))

##############################################################################


def get_bus(name="SYS"):
  return broker().bus(name)
