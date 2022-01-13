import unittest
from src.validators.schema import SchemaValidator
from src.validators.number import IntegerValidator
from src.validators.string import StringValidator

class TestSchemaValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.s_keys_1 = SchemaValidator("a", IntegerValidator)
        self.s_keys_2 = SchemaValidator(("b", "c"), StringValidator)
        self.s1 = SchemaValidator({'a': StringValidator, 'nested': self.s_keys_1 })
        self.s2 = SchemaValidator({'b': IntegerValidator, 'nested': self.s_keys_2 })
        self.s1_s2 = self.s1 + self.s2
        self.s3 = self.s1 | self.s2
        self.s4 = self.s_keys_1 & self.s_keys_2

    def test_valid_schema(self):
        self.assertTrue(self.s_keys_1.validate({'a': 15}))
        self.assertTrue(self.s_keys_1.validate({'a': -100, 'b': 50}))
        self.assertTrue(self.s_keys_2.validate({'a': 15, 'b': "hello", "c": "help"}))
        self.assertTrue(self.s1.validate({'a': "hello", 'nested': {'a': 15}}))
        self.assertTrue(self.s2.validate({'b': 14, 'nested': {'b': "hello", "c": "help"}}))
        self.assertTrue(self.s1_s2.validate({'a': "hello", 'b': 14, 'nested': {'b': "hello", "c": "help"}}))
        self.assertTrue(self.s3.validate({'a': "hello", 'nested': {'a': 15}}))
        self.assertTrue(self.s3.validate({'b': 14, 'nested': {'b': "hello", "c": "help"}}))
        self.assertTrue(self.s3.validate({'a': "hello", 'b': 14, 'nested': {'b': "hello", "c": "help"}}))
        self.assertTrue(self.s4.validate({'a': -100, 'b': "hello", "c": "help"}))

    def test_invalid_schema(self):
        self.assertFalse(self.s_keys_1.validate(123))
        self.assertFalse(self.s_keys_1.validate("hello"))
        self.assertFalse(self.s_keys_1.validate([]))
        self.assertFalse(self.s_keys_1.validate(()))
        self.assertFalse(self.s_keys_1.validate(True))
        self.assertFalse(self.s_keys_1.validate({'key': 15}))
        self.assertFalse(self.s_keys_1.validate({'a': 'hello'}))
        self.assertFalse(self.s_keys_1.validate({'a': 'hello', 'key': 15}))
        self.assertFalse(self.s1_s2.validate({'a': "hello", 'nested': {'a': 15}}))
        self.assertFalse(self.s1_s2.validate({'b': 14, 'nested': {'a': -100, 'b': 50}}))
        self.assertFalse(self.s4.validate({'a': 15}))
        self.assertFalse(self.s4.validate({'a': -100, 'b': 50}))
        self.assertFalse(self.s4.validate({'b': "hello", "c": "help"}))
        

def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSchemaValidator))
    
    return suite