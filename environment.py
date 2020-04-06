import os
import importlib.util


def load_env_vars():
    if os.environ['FLASK_ENV'] == 'development':
        spec = importlib.util.spec_from_file_location("development_vars.load_vars", "development_vars.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.load_vars(os)
