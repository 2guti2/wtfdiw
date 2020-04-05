import glob
import unittest

test_files = glob.glob('*/__tests__/test_*.py')
module_strings = [test_file[0:len(test_file)-3] for test_file in test_files]
module_names = []
for module_string in module_strings:
    module_names.append(module_string.replace('/', '.'))
suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_names]
test_suite = unittest.TestSuite(suites)
test_runner = unittest.TextTestRunner(verbosity=2).run(test_suite)
