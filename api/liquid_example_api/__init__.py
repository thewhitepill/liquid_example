from typing import get_args

from pydantic_core import core_schema
from pyrsistent import PMap, pmap


@classmethod
def _get_pmap_pydantic_core_schema(cls, source_type, handler):
    key_type, value_type = get_args(source_type)

    return core_schema.no_info_after_validator_function(
        pmap,
        core_schema.dict_schema(
            handler(key_type),
            handler(value_type)
        ),
        serialization=core_schema.plain_serializer_function_ser_schema(
            dict,
            info_arg=False,
            return_schema=core_schema.dict_schema(
                handler(key_type),
                handler(value_type)
            )
        )
    )


PMap.__get_pydantic_core_schema__ = _get_pmap_pydantic_core_schema
