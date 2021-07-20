from argparse import ArgumentParser, FileType
from sys import stdin
from json import load

def codegen():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_codegen = subparsers.add_parser('codegen')
    parser_codegen.add_argument('infile', nargs='?', type=FileType('r'), default=stdin)
    parser_codegen.add_argument('name', nargs=1, type=str)


    parsed = parser.parse_args()
    json_schema = load(parsed.infile)
    generate(json_schema, parsed.name[0])


def header():
    print(
        """
# This code is automagically generated using jsonschema-marshmallow
#
# https://github.com/gijzelaerr/jsonschema-marshmallow
#
from marshmallow import Schema, fields

"""
    )


mapping = {
    'string': "fields.String",
    'integer': "fields.Integer",
    'boolean': "fields.Boolean",
    'number': "fields.Float",
    'null': "fields.Field",  # todo: see if there is a better solution for this
}


def convert(entry: dict, required: bool = False) -> str:
    if '$ref' in entry:
        name = entry['$ref'][14:]
        return f"fields.Nested({name})"
    if 'const' in entry:
        return f"fields.Constant(constant=\"{entry['const']}\")"
    elif 'type' in entry:
        type_ = entry['type']
        if type_ == 'object':
            return f"fields.Nested(NotImplementedYet, required={required})"
        elif type_ == 'array':
            if 'items' in entry:
                array_type = "NotImplementedYet"
            else:
                array_type = "fields.Field"
            return f"fields.List({array_type}, required={required})"
        if type(type_) == list:
            return f"fields.Nested(NotImplementedYet)"  # todo: use UnionField for this
        elif type_ in mapping:
            return f"{mapping[type_]}(required={required})"
        else:
            return f"fields.Nested(NotImplementedYet)"


def generate(json_schema: dict, schema_name: str):
    header()

    if 'definitions' in json_schema:
        print("# definitions")
        for def_name, def_obj in json_schema['definitions'].items():
            assert(def_obj['type'] == 'object')
            print(f"class {def_name}(Schema):")
            for prop_name, prop_value in def_obj['properties'].items():
                line = convert(prop_value)
                print(f"    {prop_name} = {line}")
            print("\n")

    requireds = json_schema.get('required', [])
    if 'properties' in json_schema:
        print("# properties")
        print(f"class {schema_name}(Schema):")
        for prop_name, prop_value in json_schema['properties'].items():

            if 'type' in prop_value or 'const' in prop_value:
                required = prop_name in requireds
                line = convert(prop_value, required)

            elif 'anyOf' in prop_value:
                for entry in prop_value['anyOf']:
                    line = convert(entry)  # todo: use union
            else:
                raise NotImplementedError
            print(f"    {prop_name} = {line}")
        print("\n")


if __name__ == '__main__':
    codegen()
