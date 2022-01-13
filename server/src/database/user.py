from typing import Literal, Optional
from src.database.core import DatabaseNode, update_parent
from src.database.macros import IMacroSplit, Macros
from src.schemas.collection import Collection
from src.schemas.meal import IMeal
from src.schemas.user import ICreateUser, IFollowOptions, IUpdateUser, IUser, IWeightDateGoal
from src.utils.units import HeightCm, HeightFtIn, WeightKg, WeightLb

default_user_dict: IUser = {
    'id': 0,
    'username': "",
    'password': "",
    'name': "",
    'weight': {'value': 0, 'kind': 'kg'},
    'goal': 'maintain',
    'activity_level': 'sedentary',
    'age': 0,
    'gender': 'm',
    'height': {'value': 0, 'kind': 'cm'},
    'target_macros': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
    'current_macros': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0},
    'macro_split': None,
    'meals': Collection(),
    'following': Collection(),
    'followers': Collection(),
    'weight_date_goal': None
}

class User(DatabaseNode[IUser]):
    def __init__(self, user: ICreateUser | IUser = default_user_dict) -> None:
        super().__init__()
        self.initialize(user)
    
    @update_parent
    def update_user(self, u: IUpdateUser):
        self.name = u.get('name', self.name)
        self.weight = u.get('weight', self.weight)
        self.goal = u.get('goal', self.goal)
        self.activity_level = u.get('activity_level', self.activity_level)
        self.age = u.get('age', self.age)
        self.gender = u.get('gender', self.gender)
        self.height = u.get('height', self.height)
        self.macro_split = u.get('macro_split', self.macro_split)
        self.weight_date_goal = u.get('weight_date_goal', self.weight_date_goal)

    @update_parent
    def add_meal(self, meal: IMeal):
        self.meals[meal['name']] = meal
            
    @update_parent
    def follow(self, user: 'User', follow_options: IFollowOptions):
        self.following[user.username] = follow_options
        user.followers[self.username] = follow_options

    @update_parent
    def unfollow(self, user: 'User'):
        del self.following[user.username]
        del user.followers[self.username]

    def initialize(self, dict: IUser | ICreateUser):
        self.id: int = dict.get('id', default_user_dict['id'])
        self.username: str = dict['username']
        self.password: str = dict['password']
        self.name: str = dict.get('name', default_user_dict['name'])
        self.weight: WeightKg | WeightLb = dict.get('weight', default_user_dict['weight'])
        self.goal: Literal['gain', 'loss', 'maintain'] = dict.get('goal', default_user_dict['goal'])
        self.activity_level: Literal['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active'] = dict.get('activity_level', default_user_dict['activity_level'])
        self.age: int = dict.get('age', default_user_dict['age'])
        self.gender: Literal['m', 'f'] = dict.get('gender', default_user_dict['gender'])
        self.height: HeightCm | HeightFtIn = dict.get('height', default_user_dict['height'])
        self.target_macros: Macros = Macros.deserialize(dict.get('target_macros', default_user_dict['target_macros'])).link(self)
        self.current_macros: Macros = Macros.deserialize(dict.get('current_macros', default_user_dict['current_macros'])).link(self)
        self.macro_split: Optional[IMacroSplit] = dict.get('macro_split', default_user_dict['macro_split'])
        self.meals: Collection[IMeal] = dict.get('meals', default_user_dict['meals'])
        self.following: Collection[IFollowOptions] = dict.get('following', default_user_dict['following'])
        self.followers: Collection[IFollowOptions] = dict.get('followers', default_user_dict['followers'])
        self.weight_date_goal: Optional[IWeightDateGoal] = dict.get('weight_date_goal', default_user_dict['weight_date_goal'])

    def serialize(self) -> IUser:
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'name': self.name,
            'weight': self.weight,
            'goal': self.goal,
            'activity_level': self.activity_level,
            'age': self.age,
            'gender': self.gender,
            'height': self.height,
            'target_macros': self.target_macros.serialize(),
            'current_macros': self.current_macros.serialize(),
            'macro_split': self.macro_split,
            'meals': self.meals,
            'following': self.following,
            'followers': self.followers,
            'weight_date_goal': self.weight_date_goal
        }

    @staticmethod
    def deserialize(dict: IUser) -> 'User':
        return User(dict)