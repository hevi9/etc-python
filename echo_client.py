#!/usr/bin/env python3.4
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-protocol.html

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio

class EchoClient(asyncio.Protocol):
  message = 'This is the message. It will be echoed.'

  def connection_made(self, transport):
    transport.write(self.message.encode())
    print('data sent: {}'.format(self.message))

  def data_received(self, data):
    print('data received: {}'.format(data.decode()))

  def connection_lost(self, exc):
    print('server closed the connection')
    asyncio.get_event_loop().stop()


def main():
  logging.basicConfig(level=logging.DEBUG)
  loop = asyncio.get_event_loop()
  coro = loop.create_connection(EchoClient, '127.0.0.1', 8888)
  loop.run_until_complete(coro) # run connection
  loop.run_forever()
  loop.close()
  D("done.")


if __name__ == "__main__":
  main()
