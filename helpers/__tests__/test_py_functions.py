import unittest
from helpers.py_functions import merge_two_dicts


class PyFunctions(unittest.TestCase):
    def test_merge_two_dicts(self):
        dict1 = {'a': 1}
        dict2 = {'b': 2}
        expected_result = {'a': 1, 'b': 2}
        self.assertEqual(merge_two_dicts(dict1, dict2), expected_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
