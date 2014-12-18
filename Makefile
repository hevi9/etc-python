## things Makefile
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

include INFO

RMALL = rm -rf
RM = rm -f
CPALL = cp -au
PY3 = python3
PIP3 = pip3
SPHINX = sphinx-build
PEP8 = pep8 --first --show-source --show-pep8
PYLINT = pylint  --rcfile=setup.cfg
PYTEST = py.test -qq

cache = ./build
prefix=/usr/local
public_html = $(HOME)/public_html/$(name)
github = http://github.com/hevi9/$(name)
ghpages = $(cache)/ghpages

modules = $(sort $(wildcard $(name)/*.py))
pycaches = $(shell find . -name __pycache__) 


##############################################################################

.PHONY: install develop test clean public_html ghpages

help::
	@echo Targets:
	@echo "  install     - install files into $(prefix)"
	@echo "  develop     - install as development mode (symlinks)"
	@echo "  test        - run tests"
	@echo "  clean       - clean generated build files"
	@echo "  public_html - build documentation to $(public_html)"
	@echo "  ghpages     - build documentation to github pages $(github)"
	@echo "  pep8        - check PEP8 python code style"
	@echo "  lint        - check pytcon code style and correcteness"
	@echo "  style       - python code checks"
	@echo "  check       - validate project"

##############################################################################

install:
	$(PIP3) install .

develop:
	$(PIP3) install -r requirements-dev.txt -e .

test-unit:
	$(PY3) -m unittest discover -s test -v
  
test::
	$(PYTEST)
	
clean::
	$(RMALL) build
	$(RMALL) dist
	$(RMALL) $(name).egg-info
	$(RMALL) $(pycaches)
  
html:
	$(SPHINX) -b html -d $(cache)/doctrees ./doc $(cache)/html
  
public_html: html
	$(CPALL) $(cache)/html/. $(public_html)
  
ghpages:
	mkdir -p build
	-git clone --single-branch --branch gh-pages $(github) $(ghpages)
	$(SPHINX) -b html -d $(cache)/doctrees ./doc $(ghpages)
	cd $(ghpages) && git add .
	cd $(ghpages) && git commit -a -m "Auto update"
	cd $(ghpages) && git push origin gh-pages

pep8::
	$(PEP8) $(name)
	
lint::
	$(PYLINT) $(name)

style:: pep8 lint

check:: style test
