from pydantic_core import core_schema
from pyrsistent import PMap, pmap


@classmethod
def _get_pmap_pydantic_core_schema(cls, source_type, handler):
    return core_schema.no_info_after_validator_function(
        pmap,
        core_schema.dict_schema()
    )


PMap.__get_pydantic_core_schema__ = _get_pmap_pydantic_core_schema
