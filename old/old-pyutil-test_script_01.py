#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
## $Id: test_script_01.py,v 1.15 2005-09-06 11:54:17 hevi Exp $
## UNITTEST

"""
"""

######################################################################
## dependencies

import unittest
import os

j = os.path.join

import pyutil.script

scr = pyutil.script.Script()
ff = scr
Path = pyutil.script.Path

######################################################################
## config

root = "/tmp/pyutil_test"

######################################################################
## tests

class TestPath(unittest.TestCase):
  
  def test_repr(self):
    assert(repr(Path("/tmp")) == "Path('/tmp')")

  def test_add(self):
    assert(Path("/tmp") + "foo" == '/tmpfoo')

  def test_radd(self):
    assert("foo" + Path("/tmp") == 'foo/tmp')
    
  def test_div(self):
    assert(Path("/tmp")/"a"/"b" == '/tmp/a/b')
    
  def test_uniq_path(self):
    assert Path("/tmp").uniq_path() == "/tmp"

  def test_normcase(self):
    assert Path("/ihQx").normcase() == "/ihQx"
  
  def test_norm_path(self):
    assert(Path("/tmp/foo/../bar").norm_path() == "/tmp/bar")
    # assert Path("/..") == "/"
      
  def test_expand_user(self):
    Path("~/foo").expand_user()
    
  def test_expand_vars(self):
    Path("/tmp/$FOO/bar").expand_vars()
    
  def test_expand(self):
    Path("~/foo/$BAR").expand()
      
  def test_exists(self):
    path = Path(root)
    path.exists()
    assert(Path("huuhaa").exists() == False)
  
  def test_is_uniq(self):
    assert(Path("/tmp").is_uniq() == True)
    assert(Path("file.txt").is_uniq() == False)
    assert(Path("./../file.txt").is_uniq() == False)

  def test_is_dir(self):
    assert Path("/tmp").is_dir() == True
    
  def test_is_reg(self):
    Path("file.txt").is_reg()
    
  def test_mountpoint(self): # file depend
    Path("/tmp").is_mountpoint()
    
  def test_can_read(self):
    Path("/tmp").can_read()

  def test_can_write(self):
    Path("/tmp").can_write()

  def test_can_exec(self):
    Path("/tmp").can_exec()

  def test_mode(self):
    Path("/tmp").access_mode()

  def test_owner(self):
    Path("/tmp").owner()

  def test_time_create(self):
    Path("/tmp").time_create()

  def test_time_access(self):
    Path("/tmp").time_access()

  def test_time_modify(self):
    Path("/tmp").time_modify()

  def test_size(self):
    Path("/tmp").size()
    
  def test_list(self):
    tmp = Path("/tmp")
    tmp.list()
  
  def test_mountpoint(self):
    p = Path(os.getcwd())
    #print p,p.mountpoint()
    p = Path("/")
    #print p,p.mountpoint()
    p = Path("/tmp")
    #print p,p.mountpoint()
    p = Path("foo/bar")
    #print p,p.mountpoint()
    
  def test_nodes(self):
    ## absolute
    assert Path("/").nodes()        == ["/"]
    assert Path("/tmp").nodes()     == ["/","tmp"]
    assert Path("/usr/bin").nodes() == ["/","usr","bin"]
    ## relative 
    assert Path("build").nodes()     == ["build"]
    assert Path("build/bin").nodes() == ["build","bin"]
    assert Path("./onedot").nodes()  == [".","onedot"]
    assert Path("../twodot").nodes() == ["..","twodot"]
    assert Path(".").nodes()         == ["."]
    assert Path("..").nodes()        == [".."]
    assert Path("../").nodes()       == [".."]
    ## absurd, does not exist, but no the nodes() job to care
    assert Path("/..").nodes()       == ["/",".."]
    ## extra chars
    assert Path("trailing/slash/").nodes() == ["trailing","slash"]
    ## existence
    assert Path(Path("/usr/bin").nodes()[0]).exists()
    ## errors
    try:
      Path("").nodes()
    except SyntaxError:
      pass
    else:
      assert False,"should raise SyntaxError"

  def test_common_path(self):
    ## unique (absolute)
    assert Path("/").common_path("/") == ("/","","")
    assert Path("/usr").common_path("/tmp") == ("/","usr","tmp")
    ## relative
    assert Path("wrk/test/Mod").common_path("wrk/test/Mod1") == \
      ("wrk/test","Mod","Mod1")
    assert Path("../.././foo/bar").common_path("../../foo/xyzzy/a") == \
      ("../../foo","bar","xyzzy/a")
    assert Path("yes/tmp").common_path("no/tmp") == ("","yes/tmp","no/tmp")
    
  def test_rel_path(self):
    
    assert Path("").rel_path("") == "."    
    assert Path(".").rel_path(".") == "."    
    assert Path("..").rel_path("..") == "."    
    assert Path(".").rel_path("..") == ".."    
    Path("..").rel_path(".") == "" # error, cannot know

    assert Path("/a/b/c/d").rel_path("") == "."     
    
    ## uniq to uniq   
    assert Path("/a/b/c/d").rel_path("/") == "../../../.."        
    assert Path("/a/b/c/d").rel_path("/a") == "../../.."    
    assert Path("/a/b/c/d").rel_path("/a/b") == "../.."    
    assert Path("/a/b/c/d").rel_path("/a/b/c") == ".."    
    assert Path("/a/b/c/d").rel_path("/a/b/c/d") == "."    
    ## uniq to uniq
    assert Path("/a/b/c/d").rel_path("/a/b/c/d") == "."    
    assert Path("/a/b/c").rel_path("/a/b/c/d") == "d"    
    assert Path("/a/b").rel_path("/a/b/c/d") == "c/d"    
    assert Path("/a").rel_path("/a/b/c/d") == "b/c/d"    
    assert Path("/").rel_path("/a/b/c/d") == "a/b/c/d"    
    
    
    ## rel to rel
    assert Path("a/b/c/d").rel_path("a/b/c/d") == "."    

    assert Path("a/b/c").rel_path("a/b/c/d") == "d"    
    assert Path("a/b").rel_path("a/b/c/d") == "c/d"    
    assert Path("a").rel_path("a/b/c/d") == "b/c/d"    

    assert Path("a/b/c/d").rel_path("a/b/c") == ".."    
    assert Path("a/b/c/d").rel_path("a/b") == "../.."    
    assert Path("a/b/c/d").rel_path("a") == "../../.."    

    assert Path("a/b").rel_path('../../a1/b1/c1/d1/file3') == '../../../../a1/b1/c1/d1/file3'

    ## uniq to rel, simple
    assert Path("/tmp/foo").rel_path('a/b/file2') == 'a/b/file2'
    assert Path("/tmp/foo").rel_path('../../file1') == '../../file1'
    assert Path("/a/b/").rel_path('../../file1') == '../../file1'

    ## rel to uniq => error
    #assert Path("a/b").rel_path('/tmp/foo/../../a1/b1/c1/d1/file3') =='../../a1/b1/c1/d1/file3'
    assert Path("a/b").rel_path("/a/b/c/d") == "/a/b/c/d"
    assert Path("").rel_path("/a/b/c/d") == "/a/b/c/d" # error, cannot know    

######################################################################
## tests

class TestPathNameParts(unittest.TestCase):

  def test_dir(self):
    ## unique
    assert Path("/a").dir() == "/"
    assert Path("/a/b").dir() == "/a"
    assert Path("/a/b/c").dir() == "/a/b"
    assert Path("/a/b/c/d").dir() == "/a/b/c"
    ## relative
    #print ">>>",Path("a").dir()
    assert Path("a").dir() == ""
    assert Path("a/b").dir() == "a"
    assert Path("a/b/c").dir() == "a/b"
    assert Path("a/b/c/d").dir() == "a/b/c"
    ## going up
    # print Path(".").dir()
    assert Path(".").dir() == ".."
    assert Path("..").dir() == "../.."
    assert Path("../..").dir() == "../../.."
    assert Path("../a").dir() == ".."
    assert Path("../a/..").dir() == "../.."
    assert Path("../a/../..").dir() == "../../.."
    assert Path("../a/./..").dir() == "../.."
    ##
    #print Path("/").dir()
    #assert Path("/").dir() == "/" # convention
    assert Path("/").dir() == None # return None is now more relevant

  def test_name(self):
    assert Path("/a").name() == "a"
    assert Path("/a/b").name() == "b"
    assert Path("a").name() == "a"
    assert Path("a/b").name() == "b"
    #assert Path("").name() == "" or "." ?
    assert Path(".") == "."
    assert Path("..") == ".."    

  def test_ext(self):
    ## without nodot
    assert Path("python.py").ext() == ".py"
    assert Path("/tmp").ext()      == ""
    assert Path(".coverage").ext() == ".coverage"
    assert Path("/tmp/package-1.2.3.tar.gz").ext() == ".gz"
    ## with nodot
    assert Path("python.py").ext(nodot=True) == "py"
    assert Path("/tmp").ext(nodot=True)      == ""
    assert Path(".coverage").ext(nodot=True) == "coverage"
    assert Path("/tmp/package-1.2.3.tar.gz").ext(nodot=True) == "gz"

  def test_base(self):
    assert Path("/tmp/package-1.2.3.tar.gz").base() == "package-1.2.3.tar"    

  def test_drive(self):
    Path("C:/joo").drive()

  def test_base_ext(self):
    assert Path("/tmp/package-1.2.3.tar.gz").base_ext() == \
    ("package-1.2.3.tar",".gz")

  def test_dir_base_ext(self):
    assert Path("/tmp/package-1.2.3.tar.gz").dir_base_ext() == \
    ("/tmp","package-1.2.3.tar",".gz")

  def test_dir_name(self):
    assert Path("/foo/bar").dir_name() == ("/foo","bar")
      
    
######################################################################
## test Script
    
class TestScript(unittest.TestCase):
  """ """
  
  dir = 1
  reg = 2

  files = (
    (dir,"dira"),
    (dir,"dirb"),
    (reg,"dira/filea")
  )

  def create_dir(self,dir,mode=0755):
    try:
      os.makedirs(dir,mode)
    except:
      pass
    
  def create_file(self,file):
    fd = open(file,"w")
    fd.write("\n")
    fd.close()
        
  def create_symlink(self,file,to):
    try:
      os.remove(file)
    except OSError:
      pass
    os.symlink(to,file)
        
  def create_area(self):
    for file in TestScript.files:
      if file[0] == TestScript.dir:
        self.create_dir(j(root,file[1]))
      else:
        self.create_file(j(root,file[1]))

  def test_find(self):
    """  """
    self.create_area()
    for spec in TestScript.files:
      assert os.path.join(root,spec[1]) in scr.find(root)
    assert root in scr.find(root)

  def test_find_more(self):
    pass
    # no follow & no cross mount
    
    # no follow & cross mount
    
    # follow & no cross mount
    
    # follow & cross mount

  def test_find_brokenlink(self):
    ## setup
    self.create_dir(j(root,"dirc"))
    self.create_symlink(j(root,"dirc","aSymLink"),"no/where")
    ## test broken link case, go in error function
    self.kilroy = False
    def onerror(file,e):
      self.kilroy = True
    for path in scr.find(root,follow=True,onerror=onerror):
      pass
    assert(self.kilroy)
    ## test broken link, raise given exception in error function
    def onerror(file,e):
      raise e
    try:
      for path in scr.find(root,follow=True,onerror=onerror):
        pass
    except:
      pass
    else:
      assert(False)
  
  def test_find_nonexists_top(self):
    def onerror(f,e): pass
    for path in scr.find("foo/bar/from/outer/space",onerror=onerror):
      pass
    for path in scr.find(Path("foo/bar/from/outer/space"),onerror=onerror):
      pass

  def test_find_wide(self,depth=False):
    """ test imports """

  def test_find_follow(self,follow=True):
    """ test imports """

  def test_is_same_filesystem(self):
    p1 = Path(os.getcwd())
    p2 = Path("/")
    p3 = Path("/tmp")
    scr.is_same_filesystem()
    scr.is_same_filesystem(p1)
    scr.is_same_filesystem(p1,p2)
    scr.is_same_filesystem(p1,p2,p3)
    ##
    # TODO: make better scr.is_same_filesystem("/","/tmp","foo/bar")
    ##
    assert scr.is_same_filesystem(os.getcwd(),os.getcwd()) == True

  def test_is_same_file(self):
    assert scr.is_same_file() == True
    assert scr.is_same_file("/") == True    
    assert scr.is_same_file("/","/") == True
    assert scr.is_same_file("/","/","/") == True
    assert scr.is_same_file("/","foo/bar","/") == False
    assert scr.is_same_file("foo/bar") == False
    # TODO add linking tests

def create_dir(dir,mode=0755):
  try:
    os.makedirs(dir,mode)
  except:
    pass
  return dir 
    
def create_file(file):
  fd = open(file,"w")
  fd.write("\n")
  fd.close()
  return file

j = os.path.join

class TestFind(unittest.TestCase):
  
  def setUp(self):
    top = create_dir(j(root,"findtest"))
    f1 = create_file(j(top,"file1.txt"))
    # oo = only one
    self.oodir = create_dir(j(top,"oodir"))
    self.oofile = create_file(j(self.oodir,"afile"))
    
    
  def tearDown(self):
    pass

  def test_relative(self):
    """ find gives relative paths """
    count = 0
    file = None
    for i in ff.find(self.oodir):
      #print i
      if os.path.isfile(i):
        file = i
      count += 1
    # top dir and file
    assert count == 2,"count is %d" % count
    assert file == os.path.basename(self.oofile), "file is %s" % file
    

          
######################################################################
## running

if __name__ == '__main__':
  unittest.main()

######################################################################
# Local Variables:
# mode: python
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
