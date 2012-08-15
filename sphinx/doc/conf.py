## path definitions are reative to package root (where Makefile is run)

import sys

## sphinx
extensions = [
  'sphinx.ext.autodoc', 
  'sphinx.ext.doctest', 
  'sphinx.ext.intersphinx', 
  'sphinx.ext.todo', 
  'sphinx.ext.coverage', 
  'sphinx.ext.viewcode']
source_suffix = ".txt"
master_doc = "index"
templates_path = ['doc']
sys.path.append(".")

todo_include_todos = True

## autodoc
autodoc_default_flags = [
  'members', 
  'undoc-members', 
  'private-members', 
  'no-special-members', 
  'inherited-members',
  'show-inheritance'
]

## project
project = "learning_python3/sphinx"
version = "0.0"

## formatting
add_function_parentheses = True
add_module_names = True
pygments_style = 'sphinx'

## html output
html_theme = 'default'
#html_logo = None
#html_favicon = None
#html_static_path = ['doc']
html_last_updated_fmt = '%b %d, %Y'