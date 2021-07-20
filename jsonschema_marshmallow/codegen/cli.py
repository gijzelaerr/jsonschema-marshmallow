from argparse import ArgumentParser, FileType
from json import load
from sys import stdin

from jsonschema_marshmallow.codegen.format import format_
from jsonschema_marshmallow.codegen.extract import extract_schemas


def codegen():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_codegen = subparsers.add_parser('codegen')
    parser_codegen.add_argument('infile', nargs='?', type=FileType('r'), default=stdin)
    parser_codegen.add_argument('name', nargs=1, type=str)

    parsed = parser.parse_args()
    json_schema = load(parsed.infile)
    schemas = extract_schemas(json_schema, parsed.name[0])
    format_(schemas)


if __name__ == '__main__':
    codegen()
