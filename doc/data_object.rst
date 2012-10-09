Python Data Object
******************

Goals:

  * Object data memmers accessed by @properties.
  * Data members are iterable via some point.
  * Data member description access from @property.__doc__ .
  * Single point addition for new data member.
  * Object's class inheritance.
  
Usage
=====

Define datamember::

  class File:
  
    @property
    def size(self):
      """ Size of the file in bytes. """
      return self._st.st_size
      
    @property
    def mtime(self):
      """ Last modification time of the file. """
      return self._st.st_mtime      

Read data member::

  file = File("/some/path")
  print(f.size)

Iterate all data members::

  for d in file.data:
    print("  " + d)

Links
=====

http://docs.python.org/howto/descriptor.html

http://wiki.python.org/moin/PythonDecoratorLibrary

http://users.rcn.com/python/download/Descriptor.htm


