from typing import Literal, Optional, TypedDict
from src.schemas.collection import Collection
from src.schemas.macros import IMacroSplit, IMacros, IWeightDateGoal, MacroSplitValidator
from src.schemas.meal import IMeal
from src.utils.units import HeightCm, HeightFtIn, HeightUnitValidator, WeightKg, WeightLb, WeightUnitValidator
from src.validators.base import BoolValidator
from src.validators.number import PositiveIntValidator
from src.validators.schema import SchemaValidator, optional
from src.validators.string import LiteralStringValidator, RegexValidator, StringValidator

class IUsername(TypedDict):
    username: str
    
class ILoginUser(IUsername):
    password: str

class IUpdateUser(TypedDict, total=False):
    name: str
    weight: WeightKg | WeightLb
    goal: Literal['loss', 'gain', 'maintain']
    activity_level: Literal['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active']
    age: int
    gender: Literal['m', 'f']
    height: HeightCm | HeightFtIn
    macro_split: IMacroSplit
    weight_date_goal: IWeightDateGoal

class ICreateUser(ILoginUser, IUpdateUser): pass

class IFollowOptions(TypedDict):
    subscribe_to_meals: bool

class IFollowUser(IUsername):
    options: IFollowOptions

class IUser(TypedDict):
    id: int
    username: str
    password: str
    name: str
    weight: WeightKg | WeightLb
    goal: Literal['loss', 'gain', 'maintain']
    activity_level: Literal['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active']
    weight_date_goal: Optional[IWeightDateGoal]
    age: int
    gender: Literal['m', 'f']
    height: HeightCm | HeightFtIn
    target_macros: IMacros
    current_macros: IMacros
    macro_split: Optional[IMacroSplit]
    meals: Collection[IMeal]
    following: Collection[IFollowOptions]
    followers: Collection[IFollowOptions]

UpdateUserSchemaValidator = SchemaValidator(
{
    'name': optional(StringValidator),
    'weight': optional(WeightUnitValidator),
    'goal': optional(LiteralStringValidator(['loss', 'gain', 'maintain'])),
    'activity_level': optional(LiteralStringValidator(['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active'])),
    'age': optional(PositiveIntValidator),
    'gender': optional(LiteralStringValidator(['m', 'f'])),
    'height': optional(HeightUnitValidator),
    'macro_split': optional(MacroSplitValidator),
    'weight_date_goal': optional(SchemaValidator({'weight': WeightUnitValidator, 'date': RegexValidator(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$')}))
})

LoginUserSchemaValidator = SchemaValidator(
{
    'username': StringValidator,
    'password': StringValidator,
})

CreateUserSchemaValidator = LoginUserSchemaValidator + UpdateUserSchemaValidator

UsernameValidator = SchemaValidator({'username': StringValidator})
FollowOptionsValidator = SchemaValidator({'subscribe_to_meals': BoolValidator})
FollowUserValidator = UsernameValidator + SchemaValidator({'options': FollowOptionsValidator})

