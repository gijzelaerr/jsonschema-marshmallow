from typing import Dict, Any, Tuple, List

from jsonschema_marshmallow.codegen.model import RawSchema, RawField, mapping


def camel_case_schema(s: str):
    return ''.join(map(str.title, s.split('_'))) + "Schema"


def extract_field(prop_name: str, prop_value: Dict[str, Any], required: bool) -> Tuple[Dict[str, RawSchema], RawField]:
    if 'const' in prop_value:
        return {}, RawField(name=prop_name, type_="fields.Constant", required=required, nested=True)
    elif 'anyOf' in prop_value:
        anyOf_types = {x['type'] for x in prop_value['anyOf']}
        allow_none = 'null' in anyOf_types
        if allow_none:
            anyOf_types.remove('null')

        if len(anyOf_types) == 1:
            return extract_field(prop_name, {'type': anyOf_types.pop()}, required=required)
        else:
            # todo: use UnionField
            return {}, RawField(name=prop_name, type_="fields.Field", required=required, allow_none=True)
    elif 'type' not in prop_value:
        raise NotImplementedError
    else:
        type_ = prop_value['type']
        if type(type_) == list:
            if len(type_) == 2 and 'null' in type_:
                types = set(type_)
                types.remove('null')
                type_ = types.pop()
                return {}, RawField(name=prop_name, type_=mapping[type_], required=required, allow_none=True)
            else:
                raise NotImplementedError
        elif type_ in mapping:
            return {}, RawField(name=prop_name, type_=mapping[type_], required=required)
        elif type_ == 'object':
            name = camel_case_schema(prop_name)
            schemas = extract_schemas(prop_value, name)
            return schemas, RawField(name=prop_name, type_=name, required=required, nested=True)
        elif type_ == 'array':
            if 'items' in prop_value:
                if '$ref' in prop_value['items']:
                    name = camel_case_schema(prop_value['items']['$ref'][14:])
                    field = RawField(name=prop_name, type_=name, required=required, nested=True, list=True)
                    return {}, field
                elif prop_value['items']['type'] == 'object':
                    name = camel_case_schema(prop_name)
                    schemas = extract_schemas(prop_value['items'], name)
                    field = RawField(name=prop_name, type_=name, required=required, nested=True, list=True)
                    return schemas, field
                else:
                    type_ = prop_value['items']['type']
                    field = RawField(name=prop_name, type_=mapping[type_], required=required, nested=True, list=True)
                    return {}, field
            else:
                return {}, RawField(name=prop_name, type_="fields.Field", required=required, list=True)
        else:
            raise NotImplementedError


def extract_schemas(object_: dict, name: str) -> Dict[str, RawSchema]:
    fields: List[RawField] = []
    schemas: Dict[str, RawSchema] = {}

    if '$ref' in object_:
        return {}

    requireds = object_.get('required', [])

    additional_properties = object_.get('additionalProperties', False)

    if 'definitions' in object_:
        for def_name, def_value in object_['definitions'].items():
            schemas_new, field = extract_field(def_name, def_value, requireds)
            schemas.update(schemas_new)
            # fields.append(field)

    if 'properties' in object_:
        for prop_name, prop_value in object_['properties'].items():
            required = prop_name in requireds
            schemas_new, field = extract_field(prop_name, prop_value, required)
            schemas.update(schemas_new)
            fields.append(field)
    schemas[name] = RawSchema(fields=fields, additional_properties=additional_properties)
    return schemas
