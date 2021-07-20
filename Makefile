

VENV := venv

$(VENV):
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip wheel setuptools
	touch $(VENV)

$(VENV)/bin/jsonschema-marshmallow: $(VENV)
	$(VENV)/bin/pip install -e .

build/casv4.py: $(VENV)/bin/jsonschema-marshmallow examples/casV4.json
	$(VENV)/bin/jsonschema-marshmallow codegen $@

build:
	$(VENV)/bin/python -m build

clean:
	rm -rf build *.egg-info dist $(VENV)
