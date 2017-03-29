
"""
Common UI profile
=================

Can be implemented by engines:

 * Curses based terminal engine.
 
 * Graphical window system based engine.
 
 * Graphical direct framebuffer based engine.
 
 * Html page - web server based engine.
 
Cannot be implemented.

 * One-directional printer (or pdf generation) based engine.


"""

name = "common"

class Action(Control):
  """ Aka Button. """
  
class Integer(Control):
  """ Integer number modification. """
  
class Real(Control):
  """ """
  
class Complex(Control):
  """ """
  
class Boolean(Control):
  """ """
  
class String(Control):
  """ """
  
class Time(Control):
  """ """
  
class File(Control):
  """ """
  
class Color(Control):
  """ """
  
  
  
  
  
