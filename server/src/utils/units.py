
from typing import Literal, TypedDict, overload
from math import floor
from src.validators.number import PositiveNumberValidator

from src.validators.schema import SchemaValidator
from src.validators.string import LiteralStringValidator

class WeightLb(TypedDict):
    value: float
    kind: Literal['lb']

class WeightKg(TypedDict):
    value: float
    kind: Literal['kg']

class HeightCm(TypedDict):
    value: float
    kind: Literal['cm']

class HeightFtIn(TypedDict):
    value_ft: float
    value_in: float
    kind: Literal['ft_in']

Unit = WeightLb | WeightKg | HeightCm | HeightFtIn

class Converter:

    @staticmethod
    @overload
    def convert(val: WeightLb) -> WeightKg:
        ...
    
    @staticmethod
    @overload
    def convert(val: WeightKg) -> WeightLb:
        ...

    @staticmethod
    @overload
    def convert(val: HeightFtIn) -> HeightCm:
        ...

    @staticmethod
    @overload
    def convert(val: HeightCm) -> HeightFtIn:
        ...
    
    @staticmethod
    def convert(val: Unit) -> Unit:
        if val.get('kind') == 'kg':
            return { 'value': val.get('value', 0) * 2.2, 'kind': 'lb' }
        if val.get('kind') == 'lb':
            return { 'value': val.get('value', 0) / 2.2, 'kind': 'kg' }
        if val.get('kind') == 'ft_in':
            return { 'value': val.get('value_ft', 0) * 30.48 + val.get('value_in', 0) * 2.54, 'kind': 'cm' }
        if val.get('kind') == 'cm':
            feets = val.get('value', 0) / 30.48
            inches = (feets - floor(feets)) * 12
            return { 'value_ft': floor(feets), 'value_in': inches, 'kind': 'ft_in' }

        raise Exception("Cannot convert unknown unit")

    @staticmethod
    @overload
    def ensure_is(kind: Literal['kg'], val: WeightLb | WeightKg) -> WeightKg:
        ...

    @staticmethod
    @overload
    def ensure_is(kind: Literal['lb'], val: WeightLb | WeightKg) -> WeightLb:
        ...

    @staticmethod
    @overload
    def ensure_is(kind: Literal['cm'], val: HeightCm | HeightFtIn) -> HeightCm:
        ...

    @staticmethod
    @overload
    def ensure_is(kind: Literal['ft_in'], val: HeightCm | HeightFtIn) -> HeightFtIn:
        ...

    @staticmethod
    def ensure_is(kind: Literal['kg', 'lb', 'cm', 'ft_in'], val: Unit) -> Unit:
        if (kind != val.get('kind')):
            return Converter.convert(val)
        return val

HeightUnitValidator = (
    SchemaValidator({ 'kind': LiteralStringValidator(['cm']),'value': PositiveNumberValidator}) |
    SchemaValidator({ 'kind': LiteralStringValidator(['ft_in']),'value_ft': PositiveNumberValidator, 'value_in': PositiveNumberValidator})
)

WeightUnitValidator = SchemaValidator({ 'kind': LiteralStringValidator(['kg', 'lb']),'value': PositiveNumberValidator})