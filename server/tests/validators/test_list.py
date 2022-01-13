import unittest
from src.validators.list import BoolListValidator, StringListValidator, IntegerListValidator, FloatListValidator

class TestListValidator(unittest.TestCase):
    def test_valid_list(self):
        self.assertTrue(BoolListValidator.validate([True, False]))
        self.assertTrue(StringListValidator.validate(["hello", str(123)]))
        self.assertTrue(IntegerListValidator.validate([12, 123]))
        self.assertTrue(FloatListValidator.validate([12.0, 12.7]))
        self.assertTrue(FloatListValidator.validate([]))

    def test_invalid_list(self):
        self.assertFalse(StringListValidator.validate(123))
        self.assertFalse(StringListValidator.validate("hello"))
        self.assertFalse(StringListValidator.validate(()))
        self.assertFalse(StringListValidator.validate(True))
        self.assertFalse(StringListValidator.validate(["hello", 123]))
        self.assertFalse(StringListValidator.validate([123]))
        self.assertFalse(IntegerListValidator.validate(["hello", 123]))
        self.assertFalse(IntegerListValidator.validate(["hello"]))

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestListValidator))
    
    return suite