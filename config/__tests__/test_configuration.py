import unittest

from config.configuration import ConfigurationModule, config_var_names
from helpers.py_functions import merge_two_dicts

expected_var_value = '1'


def expected_result():
    result = {}
    for var_name in config_var_names:
        result = merge_two_dicts(result, {var_name: expected_var_value})
    return result


class ConfigMock:
    def __init__(self):
        self.config_var_dict = {}

    def update(self, config_var_dict):
        self.config_var_dict = config_var_dict

    def get(self):
        return self.config_var_dict


class EnvironMock:
    @staticmethod
    def get(foo, var):
        return expected_var_value


class OsMock:
    def __init__(self):
        self.environ = EnvironMock()


class Configuration(unittest.TestCase):

    def test_configuration_loads_dict(self):
        config = ConfigMock()
        os = OsMock()

        # When
        ConfigurationModule(config, os)

        # Then
        self.assertEqual(config.config_var_dict, expected_result())


if __name__ == '__main__':
    unittest.main(verbosity=2)
