from typing import Literal, Optional, TypedDict
from src.utils.units import HeightCm, HeightFtIn, WeightKg, WeightLb
from src.validators.base import CustomValidator
from src.validators.number import PositiveFloatValidator, PositiveIntValidator
from src.validators.schema import SchemaValidator, optional

class IMacros(TypedDict):
    fat: int
    carbs: int
    protein: int
    calories: int

class IPartialMacros(IMacros, total=False):
    pass

MacroValidator = SchemaValidator(("fat", "carbs", "protein", "calories"), optional(PositiveIntValidator))

class IMacroSplit(TypedDict):
    carbs: float
    protein: float
    fat: float

MacroSplitValidator = (
    SchemaValidator(("fat", "carbs", "protein"), PositiveFloatValidator) &
    CustomValidator[IMacroSplit](lambda v: v['carbs'] + v['fat'] + v['protein'] == 1)
)

class IWeightDateGoal(TypedDict):
    weight: WeightKg | WeightLb
    date: str

class IMacroCalculation:
    gender: Literal['m', 'f']
    weight: WeightKg | WeightLb
    height: HeightCm | HeightFtIn
    age: int
    goal: Literal['loss', 'gain', 'maintain']
    activity_level: Literal['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active']
    macro_split: Optional[IMacroSplit]
    weight_date_goal: Optional[IWeightDateGoal]
