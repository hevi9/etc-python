#!/usr/bin/env python
## $Id: run.py,v 1.31 2004-01-05 11:52:56 hevi Exp $
##

"""
Program running and process management.
This is kind of reimplementation over popen2.py.
Reasons for implementation:
- manageable processes, popen2 does not provide kill() or process information
- tracking of the external program dependencies with pytils.extern module
- log tracing with pytils.log module
- "shell" like view to the programs
- "readable" startup setup for std* pipes and other parameters (vs popen[2-4])
- modified environment passing
- dryrun property to just test what program/script would do

Example: simple program run:
ls = program("ls")
ps = ls("-la")
ps.wait()

Example: simple program run in one line:
program("ls")("-la").wait()

Example: read from stdout:
ls = program("ls")
ps = ls("-1",program.stdout)
for line in ps.stdout:
  print line
ps.wait()

Example:
cc = program("gcc","-c")
ld = program(cc)
cc("-o","test.o","test.c")
ld("-o","test","test.o")

Collaborations:
- pytils.extern: this tells to the extern object witch programs
  are requested.
- pytils.log: tell logging messages to log
- pytils.null: on dryrun return processes as Null
"""

__version__ = "$Revision: 1.31 $"

__todo__ = """
5 documentation
5 study buffering issues
5 MAXFD fixed, no good, os.getdtablesize() anywhere ?
5 dryrun to globally managed property
6 should there be default environment too ?
5 piping support
5 implement changing working directory 
"""

######################################################################
## dependencies

import sys
import string
import os
from pytils.log import log
import pytils.log
import getopt
from pytils.common import *
from pytils.extern import extern
from pytils.process import process
import string

######################################################################
## configuration

MAXFD = 256 

class props:
  def __init__(self):
    self.dryrun = 0

props = props()

class options(object):

  def option_dryrun(self,arg):
    """ Do not change system"""
    pytils.run.props.dryrun = 1
    
######################################################################
# @ is type binding opeator
# - related to the metaclass
# listobjectobject = list(1,2)
# @list
# listclassobject = @list(typeparam)
# p = proc(args)
# p.wait()
# if proc(args).wait() != 0
# p = proc(args,proc.stdin)
# for i in list:
#   p.stdin.write(i)
# p.wait()
# 
# p1 = proc1(stdout)
# proc2(stdin = p1.stdout)


class program(object):
  """ Program declaration factory and process activation object.
  Usage:
  prog = program("prog")
  ps = prog(args,..[program.stdin][program.stdout][program.stderr]
            [program.execute][program.wait][env])
  ps.wait()

  Tags:
  program.stdin: redirect process stdin to this process for writing,
    available on ps.stdin
  program.stdout: redirect process stdout to this process for reading,
    available on ps.stdout
  program.stderr: redirect process stderr to this process for reading,
    available on ps.stderr
  program.execute: replace this process text with new program
  program.wait: wait completion of the new process

  """
  
  # tags, XXX: who double naming ?
  class stdin: pass
  stdin = stdin
  class stdout: pass
  stdout = stdout
  class stderr: pass
  stderr = stderr
  class execute: pass
  execute = execute
  class wait: pass
  wait = wait
  class nolog: pass
  nolog = nolog

  def __init__(self,prog,*args):
    """ program(prog@str|program [, args@object]) @program:
    Creates new program declarator factory. If prog argument
    is type as program, then that program path definition is used.
    args are optional default arguments, that are the applied every
    program call.
    """
    if type(prog) == program:
      # self.__dict__.update(prog.__dict__) ?
      self.prog = prog.prog
      self.absprog = prog.absprog
      self.args = args
    #if type(prog) == list or type(prog) == tuple:
    self.prog = prog
    self.absprog = extern.program(prog)
    self.args = args # default args, not from the same program

  def __call__(self,*args,**kwds):
    if self.absprog == None:
      raise RuntimeError("program " + self.prog + " not found")
    stdin = 0
    stdout = 0
    stderr = 0
    execute = 0
    wait = 0
    nolog = 0
    # process args
    args2 = [] # running args
    args2.append(self.absprog)
    args3 = [] # tags into default args too
    args3.extend(self.args) # default args
    args3.extend(args)      # per process args
    for arg in args3:
      if arg == program.stdin:
        stdin = 1
        continue
      if arg == program.stdout:
        stdout = 1
        continue
      if arg == program.stderr:
        stderr = 1
        continue
      if arg == program.execute:
        execute = 1
        continue
      if arg == program.wait:
        wait = 1
        continue
      if arg == program.nolog:
        nolog = 1
        continue
      args2.append(str(arg))
    # check dryrun
    if props.dryrun:
      if not nolog:
        log.info("would run:"," ".join(args2))
      return Null
    # make environment
    env = {}
    env.update(os.environ)
    env.update(kwds)
    # switch text if execute
    if execute:
      if not nolog:
        log.system("EXEC"," ".join(args2))
      os.execve(self.absprog,args2,env) # pass exceptions
    # fork
    if stdin:
      in_read,in_write = os.pipe()
    if stdout:
      out_read,out_write = os.pipe()
    if stderr:
      err_read,err_write = os.pipe()
    if not nolog:
      log.system("'" + "' '".join(args2) + "'")
    pid = os.fork() ### 8<
    if pid == 0: ### child
      # direct fds
      if stdin:
        os.dup2(in_read,0)
      if stdout:
        os.dup2(out_write,1)
      if stderr:
        os.dup2(err_write,2)
      for fd in range(3,MAXFD): # close other than std fds
        try:
          os.close(fd)
        except:
          pass
      os.execve(self.absprog,args2,env)
    ### parent
    if stdin:
      stdin = os.fdopen(in_write,"w")
      os.close(in_read)
    else:
      stdin = None
    if stdout:
      stdout = os.fdopen(out_read,"r")
      os.close(out_write)
    else:
      stdout = None
    if stderr:
      stderr = os.fdopen(err_read,"r")
      os.close(err_write)
    else:
      stderr = None
    ps = process(pid,stdin,stdout,stderr)
    if wait: # for convience
      if not nolog:
        log.debug("waiting for process",ps.pid)
      ps.wait()
    return ps

  def __str__(self):
    if not self.absprog:
      return self.prog
    if len(self.args):
      return self.absprog + " " + " ".join(map(str,self.args))
    else:
      return self.absprog

Program = program
    
######################################################################
## program_main

class program_main(object):
  """

  option_*(self)
  or
  option_*(self,arg = Default)
  
  """

  __metaclass__ = Singleton

  def __init__(self,*args,**kwds):
    """ main():
    """
    self.layout()
    args = self.parse(args)
    self.run(args)

  def parse(self,args):
    """ parse(args@seq) @seq(str), raises Unknown, syncs single, mutates:
    """
    opts_spec = list()
    for function in self._option_functions():
      option_argument = ""
      if function.im_func.func_defaults:
        option_argument = "="
      opts_spec.append(self._option_function_to_name(function)
                       + option_argument)
    try:
      opts_got,args_left = getopt.getopt(args,"",opts_spec)
    except getopt.GetoptError, e:
      self.usage(e).exit(2)
    for opt,arg in opts_got:
      function = self._option_name_to_function(opt)
      function(arg)
    return args_left

  def _option_functions(self):
    functions = list()
    for name in dir(self):
      parts = name.split("_")
      if len(parts) > 1 and parts[0] == "option":
        functions.append(getattr(self,name))
    return functions

  def _option_function_to_name(self,function):
    parts = function.__name__.split("_")
    assert(len(parts) >= 2 and parts[0] == "option")
    return "-".join(parts[1:])

  def _option_name_to_function(self,name):
    if name[:2] == "--": # remove leading --
      name = name[2:]
    name = name.translate(string.maketrans("-","_"))
    name = "option_" + name
    if not hasattr(self,name):
      raise RuntimeError("option function \"" + name + "\" not in main")
    return getattr(self,name)

  def usage_stream(self):
    return sys.stderr

  def usage(self,msg = None):
    """ usage() @self, raises Unknown, syncs single, const:
    """
    ws = self.usage_stream()
    ## write syntax error if any
    if msg:
      ws.write("Error: " + str(msg) + "\n")
    ## write syntax
    self.usage_write_syntax()
    ## write short documentation
    if hasattr(self,"__doc__") and self.__doc__ and len(self.__doc__.strip()):
      ws.write(self.__doc__.strip())
      ws.write("\n")
    ## write options if any
    if len(self._option_functions()):
      ws.write("Options:\n")
      for function in self._option_functions():
        ws.write(" --" + self._option_function_to_name(function))
        if function.im_func.func_defaults:
          ws.write("=arg (default: " + str(function.im_func.func_defaults[0])
                   + ")")
        ws.write(" : ")          
        ws.write(function.__doc__.strip())
        ws.write("\n")
    ws.write("\n")
    return self

  def usage_write_syntax(self):
    ws = self.usage_stream()
    ws.write("Usage: ")
    ws.write(os.path.basename(sys.argv[0]) + " ")
    if len(self._option_functions()):
      ws.write("[Options]" + " ")
    ws.write("[args ..]")
    ws.write("\n")
    

  def layout(self):
    """ layout() @object, raises Unknown, syncs single, mutates:
    Compose the program components.
    Returns top level object (or set of objects) of the composition.
    Have to be valled before parse().
    """
    raise NotImplementedError

  def run(self,args):
    """ run(args@seq) @void, raises Unknown, syncs single, mutates:
    """
    for arg in args:
      log.debug(arg)

  def exit(self,rc):
    """ exit(rc@int) @void, raises Unknown, syncs single, terminates:
    """
    sys.exit(rc)


# Local Variables:
# mode: python
# mode: auto-fill
# fill-column: 79
# fill-prefix: "  "
# indent-tabs-mode: nil
# py-indent-offset: 2
# End:
