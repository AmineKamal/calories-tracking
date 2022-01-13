from src.validators.base import Validator
from typing import Any, Optional

class _IntegerValidator(Validator):
    def validate(self, val: Any) -> bool:
        return isinstance(val, int) and not isinstance(val, bool)
IntegerValidator = _IntegerValidator()

class _FloatValidator(Validator):
    def validate(self, val: Any) -> bool:
        return isinstance(val, float)
FloatValidator = _FloatValidator()

class RangeValidator(Validator):
    def __init__(self, min: Optional[int], max: Optional[int]) -> None:
        super().__init__()
        self.min = min
        self.max = max

    def validate(self, val: Any) -> bool:
        return isinstance(val, int) and (self.min == None or val >= self.min) and (self.max == None or val <= self.max)

PositiveIntValidator = RangeValidator(0, None)

class FloatRangeValidator(Validator):
    def __init__(self, min: Optional[float], max: Optional[float]) -> None:
        super().__init__()
        self.min = min
        self.max = max

    def validate(self, val: Any) -> bool:
        return isinstance(val, float) and (self.min == None or val >= self.min) and (self.max == None or val <= self.max)
PositiveFloatValidator = FloatRangeValidator(0, None)

PositiveNumberValidator = PositiveIntValidator | PositiveFloatValidator