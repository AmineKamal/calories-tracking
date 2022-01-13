from src.validators.base import Validator, BoolValidator
from typing import Any, List, cast
from src.validators.number import IntegerValidator, FloatValidator
from src.validators.string import StringValidator

class ListValidator(Validator):
    def __init__(self, validator: Validator) -> None:
        super().__init__()
        self.item_validator = validator

    def validate(self, val: Any) -> bool:
        return isinstance(val, list) and all(self.item_validator.validate(e) for e in cast(List[Any], val))

IntegerListValidator = ListValidator(IntegerValidator)
StringListValidator = ListValidator(StringValidator)
FloatListValidator = ListValidator(FloatValidator)
BoolListValidator = ListValidator(BoolValidator)