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
from jsonschema_marshmallow.dynamic import convert
convert('example.json')
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