from helpers.py_functions import merge_two_dicts

config_var_names = [
    'GOOGLE_CLIENT_ID',
    'GOOGLE_CLIENT_SECRET',
    'GOOGLE_DISCOVERY_URL'
]


class ConfigurationModule:
    def __init__(self, config, os):
        self.config = config
        self.os = os
        self.__load_env()

    def __load_env(self):
        config_var_dict = {}
        for var_name in config_var_names:
            var_value = self.os.environ.get(var_name, None)
            config_var_dict = merge_two_dicts(config_var_dict, {var_name: var_value})
        self.config.update(config_var_dict)

    def get_var(self, name):
        return self.config.get(name)
