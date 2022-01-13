from datetime import datetime
from typing import cast
from src.database.core import DatabaseNode, update_parent
from src.schemas.macros import IMacroCalculation, IMacroSplit, IMacros, IPartialMacros
from src.utils.units import Converter

default_macros_dict: IMacros = {
    'fat': 0,
    'carbs': 0,
    'protein': 0,
    'calories': 0
}

class Macros(DatabaseNode[IMacros]):
    def __init__(self, macros: IMacros = default_macros_dict) -> None:
        super().__init__()
        self.initialize(macros)

    def initialize(self, m: IMacros):
        self.fat: int = m.get('fat', default_macros_dict['fat'])
        self.carbs: int = m.get('carbs', default_macros_dict['carbs'])
        self.protein: int = m.get('protein', default_macros_dict['protein'])
        self.calories: int = m.get('calories', default_macros_dict['calories'])

    @update_parent
    def update_macros(self, m: IPartialMacros):
        self.fat = m.get('fat', self.fat)
        self.carbs = m.get('carbs', self.carbs)
        self.protein = m.get('protein', self.protein)
        self.calories = m.get('calories', self.calories)

    def __add__(self, other: 'Macros'):
        m = Macros()
        
        m.calories = self.calories + other.calories
        m.protein = self.protein + other.protein
        m.fat = self.fat + other.fat
        m.carbs = self.carbs + other.carbs
        
        return m

    def __sub__(self, other: 'Macros'):
        m = Macros()
        
        m.calories = self.calories - other.calories
        m.protein = self.protein - other.protein
        m.fat = self.fat - other.fat
        m.carbs = self.carbs - other.carbs
        
        return m

    @update_parent
    def __iadd__(self, other: 'Macros'):
        self.calories += other.calories
        self.protein += other.protein
        self.fat += other.fat
        self.carbs += other.carbs

        return self

    @update_parent
    def __isub__(self, other: 'Macros'):
        self.calories -= other.calories
        self.protein -= other.protein
        self.fat -= other.fat
        self.carbs -= other.carbs

        return self

    def serialize(self) -> IMacros:
        return {
            'calories': self.calories,
            'carbs': self.carbs,
            'protein': self.protein,
            'fat': self.fat
        }

    @staticmethod
    def deserialize(dict: IMacros) -> 'Macros':
        return Macros(dict)

    @staticmethod
    def calculate_macros(params: IMacroCalculation) -> IMacros:
        w = Converter.ensure_is('kg', params.weight)
        h = Converter.ensure_is('cm', params.height)

        bmr = 10 * w['value'] + 6.25 * h['value'] - 5 * params.age + (5 if params.gender == 'm' else -161)

        if params.activity_level == 'sedentary':
            bmr *= 1.2
        elif params.activity_level == 'lightly_active':
            bmr *= 1.375
        elif params.activity_level == 'moderately_active':
            bmr *= 1.55
        elif params.activity_level == 'very_active':
            bmr *= 1.725
        else:
            bmr *= 1.9

        if params.weight_date_goal:
            to = datetime.strptime(params.weight_date_goal['date'], '%Y-%m-%d')
            now = datetime.now()
            days = (to - now).days
            target_weight = Converter.ensure_is('lb', params.weight_date_goal['weight'])['value']
            current_weight = Converter.ensure_is('lb', params.weight)['value']
            delta_calories = (target_weight - current_weight) * 3500
            calories_per_day = delta_calories / days
        else:
            if params.goal == 'loss':
                calories_per_day = -500
            elif params.goal == 'gain':
                calories_per_day = 500
            else:
                calories_per_day = 0

        bmr += calories_per_day
        
        split: IMacroSplit = params.macro_split if params.macro_split != None else cast(IMacroSplit, {
            'carbs': 0.4,
            'protein': 0.4 if params.goal == "loss" else 0.3,
            'fat': 0.2 if params.goal == 'loss' else 0.3
        })

        calories = bmr
        protein = (split['protein'] * calories) / 4
        carbs = (split['carbs'] * calories) / 4
        fat = (split['fat'] * calories) / 9

        return {'calories': round(calories), 'protein': round(protein), 'carbs': round(carbs), 'fat': round(fat) }