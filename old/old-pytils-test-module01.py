#!/usr/bin/env python
## $Id: module01.py,v 1.5 2003-08-11 19:48:34 hevi Exp $
## UNITTEST

"""
Tests for pytils.module .
"""
__version__ = "$Revision: 1.5 $"

######################################################################
## depends

import sys
import os
import unittest
import pytils.module
import pytils.file
import pytils.run

rm = pytils.run.program("rm")

######################################################################
## test material

module_a_py = """
import os
"""

module_b_py = """
import os
import a
"""

module_pkg_init_py = """
import os
"""

module_pkg_c_py = """
import os
"""

test_modules = {
  # name : (path, text)
  "a" : ("a.py",module_a_py),
  "b" : ("b.py",module_b_py),
  "pkg" : ("pkg/__init__.py",module_pkg_init_py),
  "pkg.c" : ("pkg/c.py",module_pkg_c_py)
  }

test_trash = (
  "trash_x.joo",
  "CVS/root"
  )

def write_text(text,path):
  ws = open(path,"w")
  ws.write(text)
  ws.close()

######################################################################
## test configuration
  
fs = pytils.file.FS()
root = "/tmp/pytils/tests"

######################################################################
## test Importer

class ModuleBase(unittest.TestCase):

  def setUp(self):
    self.importer = pytils.module.Importer()
    for i in test_modules:
      file = os.path.join(root,test_modules[i][0])
      fs.mkdir(os.path.dirname(file))
      write_text(test_modules[i][1],file)
    for i in test_trash:
      file = os.path.join(root,i)
      fs.mkdir(os.path.dirname(file))
      write_text("XXX\n",file)
    sys.path.append(root)
    
  def tearDown(self):
    #rm("-rf",root).wait()
    sys.path.remove(root)

######################################################################
## test Importer
  
class Importer_test(ModuleBase):

  def test_import_qname(self):
    im = self.importer
    for i in test_modules:
      #print i
      m = im.import_qname(i)

  def test_import_path(self):
    im = self.importer
    for i in test_modules:
      #print test_modules[i][0]
      m = im.import_path(test_modules[i][0])
    
  def test_find_moduleFiles(self):
    """
    """
    files = self.importer.find_moduleFiles(root)
    #print files

  def test_find_sub_moduleFiles(self):
    """
    """
    files = self.importer.find_sub_moduleFiles(root,"pkg")
    #print files

  def test_find_module(self):
    """ Test find root functionallity. """
    im = self.importer
    for i in test_modules:
      assert(im.find_module(i)[0] == root)

  def test_filetype(self):
    pass

  def test_path2qname(self):
    im = self.importer
    assert im.path2qname("package/dir/module.py") == "package.dir.module"
    assert im.path2qname("package/dir/module.pyc") == "package.dir.module"
    assert im.path2qname("package/dir/module.pyo") == "package.dir.module"
    assert im.path2qname("package/dir/module.so") == "package.dir.module"
    assert im.path2qname("package/__init__.py") == "package"

######################################################################
## test Module

class Module_test(ModuleBase):

  def test_reload(self):
    """ If reload  works """
    pass

  def test_name(self):
    """ Test getting name of the module. """
    for i in test_modules:
      module = pytils.module.Module(self.importer.import_qname(i))
      #print module.name(),i

  def test_source(self):
    """ If source of the module is correct """
    for i in test_modules:
      module = pytils.module.Module(self.importer.import_qname(i))
      #print module.source()
      assert(module.source() == os.path.join(root,test_modules[i][0]))

  def test_depends_runtime(self):
    """ That the runtime dependencies are correct """
    pass

  def test_depends_fromfile(self):
    """ That the compiled dependencies are correct """
    pass

  def test_depends(self):
    """ That the all dependencies are correct """
    for i in test_modules:
      module = self.importer.import_qname(i)
      #print module.name(),module.depends()

######################################################################
## to testing system

def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(Importer_test,'test'))
  suite.addTest(unittest.makeSuite(Module_test,'test'))
  return suite

def check():
  runner = unittest.TextTestRunner(verbosity=1)
  result = runner.run(suite())
  return not result.wasSuccessful()

if __name__ == '__main__':
  check()


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:




