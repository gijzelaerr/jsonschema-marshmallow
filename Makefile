VENV := venv
.DEFAULT_GOAL := test
.PHONY := build/casv4.py

$(VENV):
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip wheel setuptools
	touch $(VENV)

$(VENV)/bin/jsonschema-marshmallow: $(VENV)
	$(VENV)/bin/pip install -e .

build/casv4.py: $(VENV)/bin/jsonschema-marshmallow examples/casV4.json
	mkdir -p build/
	$(VENV)/bin/jsonschema-marshmallow codegen examples/casV4.json CasV4 > $@

$(VENV)/bin/mypy: $(VENV)
	$(VENV)/bin/pip install mypy

$(VENV)/bin/pycodestyle: $(VENV)
	$(VENV)/bin/pip install pycodestyle

test: build/casv4.py $(VENV)/bin/pycodestyle $(VENV)/bin/mypy
	$(VENV)/bin/mypy build/casv4.py
	$(VENV)/bin/pycodestyle build/casv4.py

build:
	$(VENV)/bin/python -m build

clean:
	rm -rf build *.egg-info dist $(VENV)
