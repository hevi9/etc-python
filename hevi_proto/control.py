"""
control -- program control information management
=================================================

Collect program **control** information into object. Access information
as namespace. Store information into .ini files if exists
with ConfigParser. Be smart on default values. 

Usage::

  ctrl = Control()
  
  if ctrl.name == 100:
    ..
    


"""

from configparser import ConfigParser