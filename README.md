# jsonschema-marshmallow
Convert JSON schemas to marshmallow schemas

# installation

```
$ pip install jsonschema-marshmallow
```

## usage

jsonschema-marshmallow has two modes, dynamic and codegen.

### dynamic mode
```python
from json import load
from jsonschema_marshmallow.dynamic import recurse

with open('casV4.json') as f:
    marshmallow = recurse(load(f))
```

output:
```python

```

### codegen mode

```shell
$ jsonschema-marshmallow codegen example.json
```

output:
```python

```