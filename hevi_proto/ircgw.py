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
    ioevents.read_add(self.fd,self.on_read)
    self.fd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.fo = self.fd.makefile("rw",1)
    D("connecting to {} .. ".format(self.addr))
    self.fd.connect(self.addr)
    D("connected")
    self.on_readline = rere.on_readline
    
  def on_readline(self,line):
    rere = self
    self = self.ctx
    D(line)
    self.writeline("PASS {}".format(self.token))
    self.writeline("NICK {}".format(self.nick))
    self.writeline("USER {} 0 * :{}".format(self.nick,self.username))
    self.on_readline = rere.on_readline2
    
  def on_readline2(self,line):
    D(line)
    

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
  
  @property
  def rfd(self):
    return self.fd
  
  def on_read(self,fd):
    D("on_read({})".format(fd))
    data = fd.recv(4096)
    D("data: {}".format(data))
    self.rbuf = self.rbuf + data.decode()
    pos = self.rbuf.find("\r\n")
    while pos > -1:
      line = self.rbuf[0:pos]
      self.on_readline(line)
      self.rbuf = self.rbuf[pos+2:]
      pos = self.rbuf.find("\r\n")
  
  def on_readline(self,line): pass # stub
  
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
    self.on_reads = dict() # fileno: (fileobject, on_read)
  
  def dispatch(self,timeout=0):
    #D("dispatch")
    #D(self.epoll.poll(timeout))
    for fd, event in self.epoll.poll(timeout):
      #D("poll: {} {}".format(fd, event))
      if event & select.EPOLLIN:
        self.on_reads[fd][1](self.on_reads[fd][0])
      
  def read_add(self, fd, on_read):
    D("read_add({},{})".format(fd,on_read))
    self.on_reads[fd.fileno()] = (fd,on_read)
    self.epoll.register(fd,select.EPOLLIN | select.EPOLLHUP)
    
  def read_remove(self,fd):
    D("read_remove({},{})".format(fd))
    self.epoll.unregister(fd)
    del self.on_reads[fd.fileno()]
      
ioevents = IOEvents()
  
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


