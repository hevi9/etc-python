from django.http import HttpResponse
from django.shortcuts import render_to_response
from hevi_util.common import *
import web.browser.system as browser

def file1(request,path):
  view_dir = "browser/view_dir1.html"
  view_reg = "browser/view_reg1.html"
  view_err = "browser/view_err1.html"
  s = browser.System()
  try:
    file = s.get_file(path)
    ctx = { "file" : file }
    if type(file) is browser.Dir:
      tmpl = view_dir
    elif type(file) is browser.Reg:
      tmpl = view_reg
    else:
      raise TypeError("not dir or reg")
  except NameError,e:
    tmpl = view_err
    ctx = {"path": path, "exp": e}
  print tmpl
  return render_to_response(tmpl,ctx)

