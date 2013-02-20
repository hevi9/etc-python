import logging # http://docs.python.org/3.2/library/logging.html
log = logging.getLogger(__name__)
import asyncore # http://docs.python.org/3.2/library/asyncore.html
import socket # http://docs.python.org/3.2/library/socket.html
import threading # http://docs.python.org/3.2/library/threading.html
import time # http://docs.python.org/3.2/library/time.html

class IOLoop(threading.Thread):
  
  def __init__(self):
    super().__init__()
    self._do_shutdown = False 
  
  def run(self):
    log.debug("IOLoop enter")
    while not self._do_shutdown:
      #log.debug("asyncore.loop enter")
      asyncore.loop(1.0)
      #log.debug("asyncore.loop leave")
    log.debug("IOLoop leave")
      
  def shutdown(self):
    if self._do_shutdown: return
    self._do_shutdown = True


class EchoClient(asyncore.dispatcher):

  def __init__(self, host, port):
    super().__init__()
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connect( (host, port) )

  def handle_connect(self):
    log.debug("handle_connect()")

  def handle_close(self):
    log.debug("handle_close()")
    self.close()

  def handle_read(self):
    log.debug("handle_read()")
    print(self.recv(8192))

logging.basicConfig(format="[%(name)s|%(threadName)s] %(message)s",level=logging.DEBUG)

ioloop = IOLoop()
ioloop.start()

client = EchoClient("localhost", 12000)
time.sleep(1)
client.send("TEST".encode())
time.sleep(1)
client.close()
time.sleep(1)

ioloop.shutdown()



