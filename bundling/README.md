# Packaging python to zip file


## Process about
```
container=./runtime
zipapp=myapp.zip

bundle:
	rm -rf $(container) $(zipapp)
	cp -r myapp $(container)
	python3 -m pip install -r requirements.txt --no-compile --target $(container)
	find $(container) -name '*.pyc' -delete
	find $(container) -type d -empty -delete
	cd $(container) && zip -r ../$(zipapp) .
```

* Have a package myapp.
  * `__main__.py` as main entry point.
* Copy myapp tree to bundle tree.
* Pip install dependent packages into bundle tree.
* Clean up bundle tree. `*.pyc` and test files.
* Zip it, so that `__main__.py` is in root.


## Notes
  * No shared library modules, `*.so` .
  * Slower execution time ~200ms than direct FS loading ~80ms.

## Links

* https://vilimpoc.org/blog/2012/11/23/bundling-up-distributable-python-package-libraries-using-pip-and-zip/
