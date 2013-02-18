#!/usr/bin/env python3

import logging # http://docs.python.org/3.2/library/logging.html
log = logging.getLogger(__name__)
import asyncore # http://docs.python.org/3.2/library/asyncore.html
import socket # http://docs.python.org/3.2/library/socket.html

##

class EchoService(asyncore.dispatcher_with_send):

  def handle_read(self):
    log.debug("handle_read()")
    data = self.recv(4096)
    log.debug("{} = self.recv(4096)".format(data))
    if data:
      self.send(data)

##

class EchoServer(asyncore.dispatcher):
  
  def __init__(self, host, port):
    super().__init__()
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.set_reuse_addr()
    self.bind((host,port))
    self.listen(5)
    
  def handle_accepted(self, sock, addr):
    log.debug("handle_accepted({}, {})".format(sock, addr))
    service = EchoService(sock)
    

##
logging.basicConfig(format="[%(name)s|%(threadName)s] %(message)s",level=logging.DEBUG)
server = EchoServer("localhost", 12000)

log.debug("asyncore.loop enter")
asyncore.loop(1.0)
log.debug("asyncore.loop leave")

