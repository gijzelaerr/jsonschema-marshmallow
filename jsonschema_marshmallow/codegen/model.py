from dataclasses import dataclass
from typing import List


@dataclass
class RawField:
    name: str
    type_: str
    required: bool = False
    nested: bool = False
    list: bool = False
    allow_none: bool = False


@dataclass
class RawSchema:
    fields: List[RawField]
    additional_properties: bool = False


mapping = {
    'string': "fields.String",
    'integer': "fields.Integer",
    'boolean': "fields.Boolean",
    'number': "fields.Float",
}