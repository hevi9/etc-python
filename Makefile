## file rules for hevi_proto

RMALL = rm -rf

prefix=/usr/local

modules = $(sort $(wildcard hevi_proto/*.py))

.PHONY: install develop

all:: develop README.rst

install:
	python3 setup.py install --prefix=$(prefix)
	
clean::
	$(RMALL) build
	$(RMALL) dist
	$(RMALL) hevi_proto.egg-info
	$(RMALL) __pycache__
	$(RMALL) hevi_proto/__pycache__
	$(RMALL) test/__pycache__
	
develop:
	python3 setup.py develop
	
README.rst: $(modules)
	python3 etc/doccat.py $(modules) > README.rst
