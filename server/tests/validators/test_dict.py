import unittest
from src.validators.number import IntegerValidator
from src.validators.string import StringValidator
from src.validators.dict import DictValidator

class TestDictValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.v1 = DictValidator(StringValidator, IntegerValidator)
        self.v2 = DictValidator(IntegerValidator, IntegerValidator)

    def test_valid_dict(self):
        self.assertTrue(self.v1.validate({'key': 15}))
        self.assertTrue(self.v1.validate({'key': 15, 'key_2': 30}))
        self.assertTrue(self.v2.validate({14: 15}))
        self.assertTrue(self.v2.validate({15: 15, 30: 30}))

    def test_invalid_dict(self):
        self.assertFalse(self.v1.validate(123))
        self.assertFalse(self.v1.validate("hello"))
        self.assertFalse(self.v1.validate([]))
        self.assertFalse(self.v1.validate(()))
        self.assertFalse(self.v1.validate(True))
        self.assertFalse(self.v2.validate({'key': 15}))
        self.assertFalse(self.v2.validate({'key': 15, 'key_2': 30}))
        self.assertFalse(self.v1.validate({14: 15}))
        self.assertFalse(self.v1.validate({15: 15, 30: 30}))

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDictValidator))
    
    return suite