## file rules for hevi_proto

RMALL = rm -rf

prefix=/usr/local

.PHONY: install develop

all:: develop

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