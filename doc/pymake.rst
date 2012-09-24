Proto: Automated file management system (pymake)
************************************************

Motivation
==========

Why use other tool than (gnu)make or cook ?

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