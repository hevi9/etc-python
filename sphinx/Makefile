package = learning_python3/sphinx
web.dir = $(HOME)/public_html
doc.dir = $(web.dir)/doc/$(package)
cache.dir = $(HOME)/.cache/sphinx_$(package)

all:: doc

doc:: public_html

web:: public_html

public_html::
	sphinx-build -C -b html -c ./doc -d $(cache.dir) . $(doc.dir)	
	