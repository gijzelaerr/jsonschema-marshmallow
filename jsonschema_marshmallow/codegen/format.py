from typing import Dict

from jsonschema_marshmallow.codegen.model import RawSchema


def header():
    print(
        """
# This code is automagically generated using jsonschema-marshmallow
#
# https://github.com/gijzelaerr/jsonschema-marshmallow
#
from marshmallow import Schema, fields, INCLUDE

"""
    )


def format_(schemas: Dict[str, RawSchema]):
    header()
    for name, schema in schemas.items():
        print(f"class {name}(Schema):")
        if schema.additional_properties:
            print("""    class Meta:\n        unknown = INCLUDE""")
        for field in schema.fields:

            extras = []
            if field.required:
                extras.append("required=True")
            if field.allow_none:
                extras.append("allow_none=True")

            if '$' in field.name:
                name = field.name.replace('$', '')
                extras.append(f"data_key='{field.name}'")
            else:
                name = field.name

            extra = ", ".join(extras)
            if field.nested and not field.list:
                if extra:
                    extra = ", " + extra
                print(f"    {name} = fields.Nested({field.type_}{extra})")
            elif field.nested and field.list:
                if extra:
                    extra = ", " + extra
                print(f"    {name} = fields.List(fields.Nested({field.type_}){extra})")
            elif not field.nested and field.list:
                if extra:
                    extra = ", " + extra
                print(f"    {name} = fields.List({field.type_}{extra})")
            else:
                print(f"    {name} = {field.type_}({extra})")

        if not schema.fields:
            print("    ...")

        print("\n")
