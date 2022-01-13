from typing import List
import unittest
from src.validators.list import IntegerListValidator
from src.validators.base import CustomValidator
from src.validators.number import IntegerValidator
from src.validators.string import StringValidator

class TestConditionalValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.int_or_str = StringValidator | IntegerValidator
        self.int_and_str = StringValidator & IntegerValidator

    def test_valid_dict(self):
        self.assertTrue(self.int_or_str.validate(15))
        self.assertTrue(self.int_or_str.validate("hello"))

    def test_invalid_dict(self):
        self.assertFalse(self.int_or_str.validate([]))
        self.assertFalse(self.int_or_str.validate(()))
        self.assertFalse(self.int_or_str.validate(True))
        self.assertFalse(self.int_and_str.validate(15))
        self.assertFalse(self.int_and_str.validate("hello"))

class TestCustomValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.sum_to_100 = IntegerListValidator & CustomValidator[List[int]](lambda l: sum(l) == 100)

    def test_valid_value(self):
        self.assertTrue(self.sum_to_100.validate([50, 50]))
        self.assertTrue(self.sum_to_100.validate([25, 25, 50]))

    def test_invalid_value(self):
        self.assertFalse(self.sum_to_100.validate(123))
        self.assertFalse(self.sum_to_100.validate("hello"))
        self.assertFalse(self.sum_to_100.validate([]))
        self.assertFalse(self.sum_to_100.validate(()))
        self.assertFalse(self.sum_to_100.validate(True))
        self.assertFalse(self.sum_to_100.validate({'key': 15}))
        self.assertFalse(self.sum_to_100.validate([98, 1]))

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConditionalValidator))
    suite.addTest(unittest.makeSuite(TestCustomValidator))
    
    return suite