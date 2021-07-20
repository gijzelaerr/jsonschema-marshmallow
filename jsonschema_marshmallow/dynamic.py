import json
from marshmallow import Schema, fields
from typing import List

mapping = {
    'string': fields.String,
    'integer': fields.Integer,
    'boolean': fields.Boolean,
    'number': fields.Float,
    'null': fields.Field,   # todo: see if there is a better solution for this
}


class UnionField(fields.Field):
    """Field that deserializes multi-type input data to app-level objects."""

    def __init__(self, val_types: List[fields.Field]):
        self.valid_types = val_types
        super().__init__()

    def _deserialize(*_, **__):
        raise NotImplementedError


def convert(entry: dict, defs: dict, required: bool = False):
    if '$ref' in entry:
        return defs[entry['$ref'][14:]]
    elif 'type' in entry:
        type_ = entry['type']
        if type_ == 'object':
            return fields.Nested(recurse(entry), required=required)
        elif type_ == 'array':
            if 'items' in entry:
                array_type = convert(entry['items'], defs)
            else:
                array_type = fields.Field
            return fields.List(array_type, required=required)
        if type(type_) == list:
            print("not implemented yet")  # todo: use UnionField for this
        elif type_ in mapping:
            return mapping[type_](required=required)
        else:
            raise NotImplementedError(type_)


def recurse(object_: dict):
    f = {}
    defs = {}
    if 'definitions' in object_:
        for k, v in object_['definitions'].items():
            defs[k] = convert(v, defs)

    requireds = object_.get('required', [])
    if 'properties' in object_:
        for k, v in object_['properties'].items():
            if 'type' in v:
                required = k in requireds
                f[k] = convert(v, defs, required)
            elif 'anyOf' in v:
                for entry in v['anyOf']:
                    f[k] = convert(entry, defs)

    return Schema.from_dict(f)


def main():
    with open('casV4.json') as f:
        schema = json.load(f)
    recurse(schema)


main()
