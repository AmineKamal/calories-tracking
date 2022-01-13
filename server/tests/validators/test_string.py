import unittest
from src.validators.string import LiteralStringValidator, RegexValidator, StringValidator

class TestStringValidator(unittest.TestCase):
    def test_valid_string(self):
        self.assertTrue(StringValidator.validate("Hello"))
        self.assertTrue(StringValidator.validate(str(123)))

    def test_invalid_string(self):
        self.assertFalse(StringValidator.validate(123))
        self.assertFalse(StringValidator.validate({}))
        self.assertFalse(StringValidator.validate([]))
        self.assertFalse(StringValidator.validate(()))
        self.assertFalse(StringValidator.validate(True))

class TestLiteralStringValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = LiteralStringValidator(['a', 'b', 'c'])

    def test_valid_string(self):
        self.assertTrue(self.validator.validate("a"))
        self.assertTrue(self.validator.validate(str("b")))
        self.assertTrue(self.validator.validate("c"))

    def test_invalid_string(self):
        self.assertFalse(self.validator.validate(123))
        self.assertFalse(self.validator.validate({}))
        self.assertFalse(self.validator.validate([]))
        self.assertFalse(self.validator.validate(()))
        self.assertFalse(self.validator.validate(True))
        self.assertFalse(self.validator.validate("hello"))

class TestRegexStringValidator(unittest.TestCase):
    def setUp(self) -> None:
        #email address validator
        self.validator = RegexValidator(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")

    def test_valid_string(self):
        self.assertTrue(self.validator.validate("test@test.com"))
        self.assertTrue(self.validator.validate("test_123@test.com"))
        self.assertTrue(self.validator.validate("t@test.ca"))

    def test_invalid_string(self):
        self.assertFalse(self.validator.validate(123))
        self.assertFalse(self.validator.validate({}))
        self.assertFalse(self.validator.validate([]))
        self.assertFalse(self.validator.validate(()))
        self.assertFalse(self.validator.validate(True))
        self.assertFalse(self.validator.validate("hello"))
        self.assertFalse(self.validator.validate("hello@"))
        self.assertFalse(self.validator.validate("@"))
        self.assertFalse(self.validator.validate("@.c"))
        self.assertFalse(self.validator.validate("v@.c"))


def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestStringValidator))
    suite.addTest(unittest.makeSuite(TestLiteralStringValidator))
    suite.addTest(unittest.makeSuite(TestRegexStringValidator))
    
    return suite