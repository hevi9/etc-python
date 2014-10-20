#!/usr/bin/env python3
## -*- coding: utf-8 -*-
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

from .data import sinfo_apply 
import socket
import ipaddress
import sys

def get_ipv4():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('google.com', 0))
  addr = s.getsockname()[0]
  s.close()
  return addr

data = {
  "name": socket.gethostname(),
  "ipv4": get_ipv4(),
  "ostype": sys.platform
  
}

sinfo_apply("host", data)
