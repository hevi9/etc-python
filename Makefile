## simeb Makefile
## Copyright (C) 2014 Petri Heinilä, LGPL 2.1

include INFO

RMALL = rm -rf
RM = rm -f
CPALL = cp -au
PY3 = python3.4
PEP8 = pep8 --first --show-source --show-pep8
PYLINT = pylint  --rcfile=setup.cfg
PIP = pip3.4

cache = ./build
prefix=/usr/local

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
	@echo "  pep8        - check PEP8 python code style"
	@echo "  lint        - check pytcon code style and correcteness"
	@echo "  style       - python code style checks"

install:
	$(PY3) setup.py install --prefix=$(prefix)

develop:
	$(PIP) install -r requirements-dev.txt -e . 

test:
	$(PY3) -m unittest discover -s test -v
	
clean::
	$(RMALL) build
	$(RMALL) dist
	$(RMALL) $(name).egg-info
	$(RMALL) $(pycaches)

pep8::
	$(PEP8) $(name)
	
lint::
	$(PYLINT) $(name)

style:: pep8 lint
