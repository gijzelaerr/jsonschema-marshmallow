from typing import List
from marshmallow import fields


class UnionField(fields.Field):
    """Field that deserializes multi-type input data to app-level objects."""

    def __init__(self, val_types: List[fields.Field]):
        self.valid_types = val_types
        super().__init__()

    def _deserialize(*_, **__):
        raise NotImplementedError
