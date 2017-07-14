PY = python3.5
PIP = $(PY) -m pip

help::
	@echo "Targets:"
	@echo "  local - Deploy local packages"

local::
	$(PIP) install -U --user -r requirements/local-pip.txt
