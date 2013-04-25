"""
mkthing - create files or trees from templates
==============================================

Usage
-----

Create single file form template::

 > mkfile afile.txt from basic.txt
  
or create empty file (same as touch)::

 > mkfile afile.txt
 
Create tree (directory) from template::

 > mkdir aproject from project
 
create tree from git::

 > mkdir aproject from git@github:user/project.git
 
or create empty directory, same as mkdir::

 > mkdir aproject

"""