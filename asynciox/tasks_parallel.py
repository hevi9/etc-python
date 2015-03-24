#!/usr/bin/env python3
## -*- coding: utf-8 -*-

# from http://docs.python.org/3.4/library/asyncio-task.html

import logging  # http://docs.python.org/py3k/library/logging.html
log = logging.getLogger(__name__)
D = log.debug
import asyncio

@asyncio.coroutine
def factorial(name, number):
  f = 1  
  for i in range(2, number+1):
    print("Task %s: Compute factorial(%s)..." % (name, i))
    yield from asyncio.sleep(1)
    f *= i
  print("Task %s: factorial(%s) = %s" % (name, number, f))


def main():
  logging.basicConfig(level=logging.DEBUG)
  tasks = [
    asyncio.Task(factorial("A",2)),
    asyncio.Task(factorial("B",3)),
    asyncio.Task(factorial("C",4))
  ]  
  loop = asyncio.get_event_loop()
  loop.run_until_complete(asyncio.wait(tasks))  
  loop.close()
  D("done.")


if __name__ == "__main__":
  main()
  