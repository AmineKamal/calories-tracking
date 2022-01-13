
from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Literal, TypeVar

class Validator(ABC):
    @abstractmethod
    def validate(self, val: Any) -> bool:
        pass

    def __and__(self, other: 'Validator'):
        if isinstance(self, ConditionalValidator) and self.condition == 'and':
            self.validators.append(other)
            conditional = self
        else:
            conditional = ConditionalValidator('and', self, other)

        return conditional

    def __or__(self, other: 'Validator'):
        if isinstance(self, ConditionalValidator) and self.condition == 'or':
            self.validators.append(other)
            conditional = self
        else:
            conditional = ConditionalValidator('or', self, other)

        return conditional

class ConditionalValidator(Validator):
    def __init__(self, condition: Literal['and', 'or'], *args: Validator) -> None:
        super().__init__()
        self.condition = condition
        self.validators = list(args)

    def validate(self, val: Any) -> bool:
        if (self.condition == 'and'):
            return all(v.validate(val) for v in self.validators)
        return any(v.validate(val) for v in self.validators)

T = TypeVar("T")
class CustomValidator(Validator, Generic[T]):
    def __init__(self, rule: Callable[[T], bool]) -> None:
        super().__init__()
        self.rule = rule

    def validate(self, val: Any) -> bool:
        return self.rule(val)
        
class _BoolValidator(Validator):
    def validate(self, val: Any) -> bool:
        return isinstance(val, bool)
BoolValidator = _BoolValidator()