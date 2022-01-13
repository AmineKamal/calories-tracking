from src.validators.base import Validator
from typing import Any, Dict, Optional, Tuple, TypedDict, cast, overload

class _SchemaKeyValidatorBase(TypedDict):
    validator: Validator
class _SchemaKeyValidatorOptional(TypedDict, total=False):
    mandatory: bool
class _SchemaKeyValidator(_SchemaKeyValidatorBase, _SchemaKeyValidatorOptional):
    pass

SchemaValidatorKeyValue = _SchemaKeyValidator | Validator

class SchemaValidator(Validator):
    @overload
    def __init__(self, schema_or_keys: str | Tuple[str, ...], validator: SchemaValidatorKeyValue) -> None:
        ...

    @overload
    def __init__(self, schema_or_keys: Dict[str, SchemaValidatorKeyValue]) -> None:
        ...

    def __init__(self, schema_or_keys: Dict[str, SchemaValidatorKeyValue] | str | Tuple[str, ...], validator: Optional[SchemaValidatorKeyValue]= None) -> None:
        super().__init__()
        self.schema = schema_or_keys if isinstance(schema_or_keys, dict) else self._create_schema(schema_or_keys, cast(SchemaValidatorKeyValue, validator))
    
    def validate(self, val: Any) -> bool:
        if not isinstance(val, dict): return False

        for k, v in self.schema.items():
            if (isinstance(v, Validator)):
                if (not k in val): return False
                if (not v.validate(val[k])): return False
            else:
                if (not k in val and v.get('mandatory', True)): return False
                if (not k in val and not v.get('mandatory', True)): continue
                if (not v.get('validator').validate(val[k])): return False
        
        return True

    def __add__(self, other: 'SchemaValidator'):
        new_schema: Dict[str, _SchemaKeyValidator | Validator] = {}

        for k, v in other.schema.items():
            new_schema[k] = v
        
        return SchemaValidator(new_schema)

    def _create_schema(self, keys: str | Tuple[str, ...], validator: SchemaValidatorKeyValue):
        schema: Dict[str, SchemaValidatorKeyValue] = dict()
        t = keys if isinstance(keys, tuple) else tuple(keys)

        for key in t:
            schema[key] = validator

        return schema

def optional(validator: Validator) -> _SchemaKeyValidator:
    return { 'validator': validator, 'mandatory': False }