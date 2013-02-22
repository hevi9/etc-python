
Python idea prototypes
**********************






Python Data Object
==================

Goals:

  * Object data memmers accessed by @properties.
  * Data members are iterable via some point.
  * Data member description access from @property.__doc__ .
  * Single point addition for new data member.
  * Object's class inheritance.
  
Usage
-----

Define datamember::

  class File:
  
    @property
    def size(self):
      ''' Size of the file in bytes. '''
      return self._st.st_size
      
    @property
    def mtime(self):
      ''' Last modification time of the file. '''
      return self._st.st_mtime      

Read data member::

  file = File("/some/path")
  print(f.size)

Iterate all data members::

  for d in file.data:
    print("  " + d)

Links
-----

http://docs.python.org/howto/descriptor.html

http://wiki.python.org/moin/PythonDecoratorLibrary

http://users.rcn.com/python/download/Descriptor.htm



 
File data access
================ 




web File browser
================



Linux /proc & /sys info discovery
=================================


Coding


Monitoring changes in /proc. /proc and inotify ?

Linux ps implementation ?

Resources


linux ps source code ? http://procps.sourceforge.net/

linux /proc /sys monitoring systems

https://github.com/seb-m/pyinotify




pyild - build management system
===============================

pyild - python build system (proto)


Goal is to collect software building scripts into
central manageable place.

Sample
------

start
::
  b('''
  git clone git://anongit.freedesktop.org/wayland/wayland
  cd wayland
  ./autogen.sh --prefix=$WLD
  make
  make install
  ''')

cd wayland is problematic

Proto: Automated file management system (pymake)
************************************************

Motivation
==========

Why use other tool than (gnu)make or cook ?

  * being able to to have programming capability as much needed in rules
    execution
  * total control: tracking every phase

Operation
=========

Basic:

1. Define and select resources (libraries and external programs)

2. Discover files and construct dependency graph

3. Execute graph by depth-first traversal with resources

Resource tracking:

1. Define and select resources (libraries and external programs)

2. List used resource: used external programs in this host, defined
   external program possibilities, used defined python pymake library
   resources 

Dependency graph tracking:

Execution tracking:

Syntax
======

sample::
  
  @rule("target.txt","source1.txt","source2.txt")
  def dummy1(ctx):
    sh.cat(ctx.srcs,ctx.trgs[0])

make comparison::
  
  target.txt: source1.txt source2.txt
    cat $@ > $$


 
Run a command on web
==================== 

WebMake
*******

Ability to run a make or other "build" commands from browser and
get build results into page.

Motivation
==========

Presentation and management of build output text.

Use
===

Start local process webappserver in current build directory::

  /wrk/project> webmake.py
  
which open browser and runs make and redirects make stdout and stderr
into web page text.

Related
=======

CI (Continuous Integration) frameworks.

Challenges
==========

ansi terminal code formatting of the output text.

recursive submakes ?

Continuous output and web-frameworks and html page structure. Producing
the make output content may take 30mins but page structure needs end
html tags immediately.   




State Machine
=============

class Sample:
  
  states = STATE("INIT","CONN","READY")
  
  states = (
    STATE(      "INIT","CONN","READY")
    IN("input1","CONN"  )
  )
  
  jj = {
    input1: ("CONN",)
  }



Template based file creation system
===================================


Motivation: speedup start of programming by giving code skeleton for
specific tasks.

Functionalities:

  * F01 File and directory instantiation from templates
  * F02 Discover roots and template directories and files
  * F03 Property data creation, automatically or by user interaction
  * F04 Simple identifier property substitution
  * F05 Instantiation valid checks, no overwriting
  * F21 (later) Complex jinja2 property substitution
  * F22 (later) Simple identifier key discovery from template files. 

Related works: alot, but not independent, build into some system.



Utilities for idea prototypes
=============================

Usage::
  from .util import *
  or
  from hevi_proto.util import *

PropsDict
---------

Iterable entry point for class properties. Properties
in enrty are readonly.

Usage::
  class MyData:
    def __init__(self):
      self.props = PropsDict(self)
      self._data = "value"
    @property
    def data(self):
      return self._value
  ..
  obj = MyData()
  for key in obj.props:
    print("{0} = {1}".format(key,obj.props[key])
    
f is for a format
-----------------

Convience format function that takes format keys directly
from locals and globals.

Usage::
  b = 100
  def func():
    a = "value"
    log.debug(f("{a} and {b}"))
    
CUI
===

Usage::





Web process list
================

Presenting linux process list in web efficient way. 

Resources

  * http://pypi.python.org/pypi/psutil
  * http://code.google.com/p/psutil/


