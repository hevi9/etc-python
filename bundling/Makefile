PY=python3
container=./runtime
zipapp=myapp.zip

help:
	@echo "Targets:"
	@echo "  bundle - create python zip bundle"
	@echo "  clean  - remove generated files"

bundle:
	rm -rf $(container) $(zipapp)
	cp -r myapp $(container)
	python3 -m pip install -r requirements.txt --no-compile --target $(container)
	find $(container) -name '*.pyc' -delete
	find $(container) -type d -empty -delete
	cd $(container) && zip -r ../$(zipapp) .

clean:
	rm -rf $(container) $(zipapp)
