from src.validators.base import Validator
from typing import Any, List
import re

class _StringValidator(Validator):
    def validate(self, val: Any) -> bool:
        return isinstance(val, str)
StringValidator = _StringValidator()

class RegexValidator(Validator):
    def __init__(self, pattern: str) -> None:
        super().__init__()
        self.pattern = pattern

    def validate(self, val: Any) -> bool:
        return isinstance(val, str) and re.fullmatch(self.pattern, val) != None

class LiteralStringValidator(Validator):
    def __init__(self, accepted_strings: List[str]) -> None:
        super().__init__()
        self.accepted_strings = accepted_strings

    def validate(self, val: Any) -> bool:
        return isinstance(val, str) and val in self.accepted_strings