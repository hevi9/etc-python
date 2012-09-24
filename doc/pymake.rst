Proto: Automated file management system (pymake)
************************************************

Operation
=========

Basic:

1. Define and select resources (libraries and external programs)

2. Discover files and construct dependency graph

3. Execute graph by depth-first traversal with resources

Syntax
======

sample::
  
  @rule("target.txt","source1.txt","source2.txt")
  def dummy1(ctx):
    sh.cat(ctx.srcs,ctx.trgs[0])

make comparison:
  
  target.txt: source1.txt source2.txt
    cat $@ > $$