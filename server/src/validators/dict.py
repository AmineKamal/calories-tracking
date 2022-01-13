from src.validators.base import Validator
from typing import Any, Dict, cast

class DictValidator(Validator):
    def __init__(self, key_validator: Validator, val_Validator: Validator) -> None:
        super().__init__()
        self.key_validator = key_validator
        self.val_validator = val_Validator

    def validate(self, val: Any) -> bool:
        if not isinstance(val, dict): return False

        for k, v in cast(Dict[Any, Any], val).items():
            if (not self.key_validator.validate(k) or not self.val_validator.validate(v)): return False

        return True


