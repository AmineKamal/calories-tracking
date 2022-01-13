import unittest
from tests.validators import test_string
from tests.validators import test_number
from tests.validators import test_dict
from tests.validators import test_list
from tests.validators import test_schema
from tests.validators import test_base

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    suites = unittest.TestSuite(
    [
        test_string.get_suite(),
        test_number.get_suite(),
        test_dict.get_suite(),
        test_list.get_suite(),
        test_schema.get_suite(),
        test_base.get_suite()
    ])
    runner.run(suites)