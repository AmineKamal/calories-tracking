from typing import TypedDict
from src.validators.number import PositiveIntValidator
from src.validators.schema import SchemaValidator
from src.validators.string import StringValidator

class IMeal(TypedDict):
    name: str
    calories: int
    protein: int
    fat: int
    carbs: int

MealValidator = SchemaValidator("name", StringValidator) + SchemaValidator(("fat", "carbs", "protein", "calories"), PositiveIntValidator)

class IMealName(TypedDict):
    name: str

MealNameValidator = SchemaValidator({'name': StringValidator})