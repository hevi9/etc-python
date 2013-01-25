RMALL = rm -rf

prefix=/usr/local

install:
	python3 setup.py install --prefix=$(prefix)
	
clean::
	$(RMALL) build
	$(RMALL) dist
	$(RMALL) hevi_proto.egg-info
	
dev:
	python3 setup.py develop