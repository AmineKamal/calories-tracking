import unittest
from src.validators.number import IntegerValidator, FloatValidator, RangeValidator, FloatRangeValidator

class TestIntegerValidator(unittest.TestCase):
    def test_valid_number(self):
        self.assertTrue(IntegerValidator.validate(100))
        self.assertTrue(IntegerValidator.validate(int(123)))
        self.assertTrue(IntegerValidator.validate(int('123')))
        self.assertTrue(IntegerValidator.validate(-123))
        
    def test_invalid_number(self):
        self.assertFalse(IntegerValidator.validate(123.0))
        self.assertFalse(IntegerValidator.validate("hello"))
        self.assertFalse(IntegerValidator.validate({}))
        self.assertFalse(IntegerValidator.validate([]))
        self.assertFalse(IntegerValidator.validate(()))
        self.assertFalse(IntegerValidator.validate(True))

class TestFloatValidator(unittest.TestCase):
    def test_valid_number(self):
        self.assertTrue(FloatValidator.validate(100.0))
        self.assertTrue(FloatValidator.validate(float(123)))
        self.assertTrue(FloatValidator.validate(float('123')))
        self.assertTrue(FloatValidator.validate(float('123.56')))
        self.assertTrue(FloatValidator.validate(-100.0))
        
    def test_invalid_number(self):
        self.assertFalse(FloatValidator.validate(123))
        self.assertFalse(FloatValidator.validate("hello"))
        self.assertFalse(FloatValidator.validate({}))
        self.assertFalse(FloatValidator.validate([]))
        self.assertFalse(FloatValidator.validate(()))
        self.assertFalse(FloatValidator.validate(True))

class TestIntegerRangeValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.r1 = RangeValidator(0, None)
        self.r2 = RangeValidator(None, 0)
        self.r3 = RangeValidator(10, 20)
        self.r4 = RangeValidator(-10, 10)

    def test_valid_range(self):
        self.assertTrue(self.r1.validate(100000000))
        self.assertTrue(self.r2.validate(-100000000))
        self.assertTrue(self.r1.validate(0))
        self.assertTrue(self.r2.validate(0))
        self.assertTrue(self.r3.validate(14))
        self.assertTrue(self.r4.validate(0))

    def test_invalid_range(self):
        self.assertFalse(self.r1.validate(-1))
        self.assertFalse(self.r2.validate(1))
        self.assertFalse(self.r3.validate(9))
        self.assertFalse(self.r3.validate(21))
        self.assertFalse(self.r4.validate(-11))
        self.assertFalse(self.r4.validate(11))

class TestFloatRangeValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.r1 = FloatRangeValidator(0, None)
        self.r2 = FloatRangeValidator(None, 0)
        self.r3 = FloatRangeValidator(10, 20)
        self.r4 = FloatRangeValidator(-10, 10)

    def test_valid_range(self):
        self.assertTrue(self.r1.validate(100000000.0))
        self.assertTrue(self.r2.validate(-100000000.0))
        self.assertTrue(self.r1.validate(0.0))
        self.assertTrue(self.r2.validate(0.0))
        self.assertTrue(self.r3.validate(14.0))
        self.assertTrue(self.r4.validate(0.0))

    def test_invalid_range(self):
        self.assertFalse(self.r1.validate(100000000))
        self.assertFalse(self.r1.validate(-1.0))
        self.assertFalse(self.r2.validate(1.0))
        self.assertFalse(self.r3.validate(9.0))
        self.assertFalse(self.r3.validate(21.0))
        self.assertFalse(self.r4.validate(-11.0))
        self.assertFalse(self.r4.validate(11.0))


def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIntegerValidator))
    suite.addTest(unittest.makeSuite(TestFloatValidator))
    suite.addTest(unittest.makeSuite(TestIntegerRangeValidator))
    suite.addTest(unittest.makeSuite(TestFloatRangeValidator))

    return suite