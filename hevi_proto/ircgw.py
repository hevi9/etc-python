#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2013 Petri Heinilä, License LGPL 2.1
""" 
Simple IRC Gateway
================== 
"""

import logging
log = logging.getLogger(__name__)
D = log.debug
logging.basicConfig(level=logging.DEBUG)
import socket
import io
import collections
import select

##############################################################################
class ReRe:
  """ Synchronized Request Reply base. """
  
  def __init__(self, ctx):
    """ ctx is a context object.
    Store request call arguments here. 
    """
    self.ctx = ctx
    self.complete = False
    self.call_done = False
    
  def on_call(self):
    pass
  
  def on_readline(self,line):
    pass
  
##############################################################################  
class Test(ReRe):
  def __init__(self,ctx): 
    super().__init__(ctx)
    
  def on_call(self): 
    D("on_call()")
    self.ctx.release = True
    
  
##############################################################################
class Connect(ReRe):
  """ Connect transport to irc server """
   
  def __init__(self,ctx): 
    super().__init__(ctx)
  
  def on_call(self):
    rere = self
    self = self.ctx
    self.fd = socket.socket()
    ioevents.on_reads[self.fd] = self.on_read
    ioevents.on_closes[self.fd] = self.on_close
    ioevents.on_writes[self.fd] = rere.on_write
    self.fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.fd.setblocking(False)
    self.fo = self.fd.makefile("rw",1)
    D("connecting to {} .. ".format(self.addr))
    try:
      self.fd.connect(self.addr)
    except BlockingIOError as ex:
      pass
    D("connected")
    self.on_reply = rere.on_reply1
        
  def on_write(self,fo):
    D("connected")
        
  def on_reply1(self,src,code,dst,rest):
    rere = self
    self = self.ctx
    if code != "020":
      raise Exception("Bad code")
    self.writeline("PASS {}".format(self.token))
    self.writeline("NICK {}".format(self.nick))
    self.writeline("USER {} 0 * :{}".format(self.nick,self.username))
    self.on_reply = rere.on_reply2
    
  def on_reply2(self,src,code,dst,rest):
    rere = self
    self = self.ctx
    D("on_reply2({},{})".format(code,rest))
    if code == 372:
      log.info(rest)
    elif code == 376:
      self.release = True      

##############################################################################
class close(ReRe):
  def __init__(self): super().__init__("close")
  def __call__(self):
    self = self.obj
    D("close()")
    self.fd.close()

##############################################################################
class Proto:
  """ Protocol for the ircserver connection. """
  
  def __init__(self,addr=("localhost",6667)):
    """
    addr is (host,port).
    """
    self.addr = addr
    self.nick = "testnick"
    self.username = "Test Code"
    self.token = "_token_" # user connection token
    self.channel = "test"
    self.release = True
    ## rere
    self.calls = collections.deque()
    ## transport things
    self.rbuf = ""
    self.fd = None
    self.reader = None
    D("Proto()")
    
  def test(self): 
    self.calls.append(Test(self))
  
  def connect(self): 
    self.calls.append(Connect(self))

  def on_write(self,fd):pass
    
  def on_close(self,fd):
    D("on_close({})".format(fd))
  
  def on_read(self,fd):
    #D("on_read({})".format(fd))
    data = fd.recv(4096)
    #D("data: {}".format(data))
    self.rbuf = self.rbuf + data.decode()
    pos = self.rbuf.find("\r\n")
    while pos > -1:
      line = self.rbuf[0:pos]
      self.on_readline(line)
      self.rbuf = self.rbuf[pos+2:]
      pos = self.rbuf.find("\r\n")
    return 1
  
  def on_readline(self,line): 
    #D(line)
    first,rest = line.split(maxsplit=1)
    if first[0] == ":": # reply ?
      src = first[1:]
      code, rest = rest.split(maxsplit=1)
      dst, rest = rest.split(maxsplit=1)
      self.on_reply(src, code, dst, rest)
    else: # cmd
      cmd = first
      self.on_cmd(cmd,rest)
      
  def on_reply(self,src,code,dst,rest): pass # stub

  def on_cmd(self,cmd,rest):
    D("cmd: {}, {}".format(cmd,rest))
    

  def writeline(self,line):
    data = (line + "\r\n").encode()
    self.fd.send(data)
  
  @property
  def load(self):
    return len(self.calls)
  
  def on_step(self):
    if self.release:
      self.release = False
      rere = self.calls.popleft()
      rere.on_call()
      
    
##############################################################################
class Stepper:
  
  def __init__(self):
    self.steps = set()
  
  def dispatch(self):
    for step in self.steps:
      if step.load > 0:
        step.on_step()
  
##############################################################################
class IOEvents:
  
  def __init__(self):
    self.epoll = select.epoll()
    self.allfos = dict() # fo: bits
    self.on_reads = IOEvents.Event(self,select.EPOLLIN,"IN")
    self.on_writes = IOEvents.Event(self,select.EPOLLOUT,"OUT") 
    self.on_closes = IOEvents.Event(self,select.EPOLLHUP,"HUP")
    self.xxxs = (self.on_reads, self.on_closes)
  
  def dispatch(self,timeout=0):
    for fd, event in self.epoll.poll(timeout):
      for xxx in self.xxxs:
        if event & xxx.event:
          for fo in xxx:
            if fo.fileno() == fd:
              more = xxx[fo](fo)
              if not more or more < 1:
                del xxx[fo]

  class Event(collections.UserDict):
    
    def __init__(self,ctx,event,name):
      self.ctx = ctx
      self.event = event
      self.name = name
      self.data = dict()

    def __setitem__(self,fo,func):
      D("__setitem__({},{})".format(fo,func))
      self.data[fo] = func
      bits = self.ctx.allfos.setdefault(fo,0)
      if bits == 0:
        self.ctx.epoll.register(fo,self.event)
      else:
        self.ctx.epoll.modify(fo,bits | self.event)
      self.ctx.allfos[fo] = bits | self.event
      
    def __delitem__(self,fo):
      D("__delitem__({})".format(fo))
      bits = self.ctx.allfos[fo] & ~self.event
      if bits == 0:
        self.ctx.epoll.unregister(fo)
        del self.ctx.allfos[fo]
      else:
        self.ctx.epoll.modify(fo,bits)
      del self.data[fo]

      
ioevents = IOEvents()


#   def dispatch(self,timeout=0):
#     #D("dispatch")
#     #D(self.epoll.poll(timeout))
#     for fd, event in self.epoll.poll(timeout):
#       #D("poll: {} {}".format(fd, event))
#       if event & select.EPOLLIN:
#         more = self.on_reads[fd][1](self.on_reads[fd][0])
#         if more < 1:
#           self.read_remove(self.on_reads[fd][0])
#       if event & self.on_hups.event:
#         for fo in self.on_hups:
#           if fo.fileno() == fd:
#             self.on_hups[fo](fo)
#   def read_add(self, fd, on_read):
#     D("read_add({},{})".format(fd,on_read))
#     self.on_reads[fd.fileno()] = (fd,on_read)
#     self.epoll.register(fd,select.EPOLLIN | select.EPOLLHUP)
#     
#   def read_remove(self,fd):
#     D("read_remove({},{})".format(fd))
#     self.epoll.unregister(fd)
#     del self.on_reads[fd.fileno()]

  
##############################################################################
def dev():
  stepper = Stepper()
  proto = Proto()
  proto.test()
  proto.connect()
  stepper.steps.add(proto)
  ##
  while True:
    stepper.dispatch()
    ioevents.dispatch()
  

  
  
if __name__ == "__main__": dev()


