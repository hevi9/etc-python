from django.http import HttpResponse
from django.shortcuts import render_to_response
import hevi_sys.control as huc
from hevi_util.common import *

import os

class File(object):
  def __init__(self,root,relpath):
    self._root = root
    self._relpath = relpath

  def name(self):
    return os.path.basename(self._relpath)

  def abspath(self):
    return os.path.join(self._root,self._relpath)

  def relpath(self):
    return self._relpath
  
  def root(self):
    return self._root

class Reg(File):
  def __init__(self,root,relpath):
    super(Reg,self).__init__(root,relpath)

class Dir(File):
  def __init__(self,root,relpath):
    super(Dir,self).__init__(root,relpath)
    
  def content(self):
    """
    return list of file
    """
    lof = list()
    for name in os.listdir(self.abspath()):
      abspath = os.path.join(self.abspath(),name)
      if(os.path.isdir(abspath)):
        file = Dir(self._root,os.path.join(self._relpath,name))
      else:
        file = Reg(self._root,os.path.join(self._relpath,name))
      lof.append(file)
    return lof
    

class System(Singleton):
  def __init__(self):
    self._root = os.environ["HOME"];
    
  def get_file(self,path):
    abspath = os.path.join(self._root,path)
    if not os.path.exists(abspath):
      raise NameError(abspath)
    if os.path.isdir(abspath):
      return Dir(self._root,path)
    else:
      return Reg(self._root,path)
      
##

def hello(request):
  return HttpResponse("Hello world")

def test1(request):
  return render_to_response("webtest/testview1.html",{})

def test2(request):
  crtl = huc.Control()
  return render_to_response("webtest/testview1.html",{})


def file1(request,path):
  view_dir = "webtest/view_dir1.html"
  view_reg = "webtest/view_reg1.html"
  view_err = "webtest/view_err1.html"
  s = System()
  try:
    file = s.get_file(path)
    ctx = { "file" : file, "name": "name"}
    if type(file) is Dir:
      tmpl = view_dir
    elif type(file) is Reg:
      tmpl = view_reg
    else:
      raise TypeError("not dir or reg")
  except NameError,e:
    tmpl = view_err
    ctx = {"path": path, "exp": e}
  return render_to_response(tmpl,ctx)

def file02(request,path):
  # path points to:
  # file
  # directory
  # error
  # * not exists
  # * no access
  s = System()
  d = s.make_dir(path)
  res = "<ul>\n"
  for file in d.content():
    res += "<li>" + file.name() + "</li>\n"
  res += "</ul>\n"    
  return HttpResponse(res)

def file01(request,path):
  return HttpResponse(path)