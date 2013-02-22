"""
Python Data Object
==================

Goals: Object data memmers accessed by @properties. Data members are iterable 
via some point. Data member description access from @property.__doc__ . Single 
point addition for new data member. Object's class inheritance.
  
Define datamember usage::

  class File:
  
    @property
    def size(self):
      ''' Size of the file in bytes. '''
      return self._st.st_size
      
    @property
    def mtime(self):
      ''' Last modification time of the file. '''
      return self._st.st_mtime      

Read data member usage::

  file = File("/some/path")
  print(f.size)

Iterate all data members usage::

  for d in file.data:
    print("  " + d)

Related::

.. _d1: http://docs.python.org/howto/descriptor.html
.. _d2: http://wiki.python.org/moin/PythonDecoratorLibrary
.. _d3: http://users.rcn.com/python/download/Descriptor.htm
"""
