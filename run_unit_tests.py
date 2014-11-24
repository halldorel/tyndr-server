#!/usr/bin/python
import optparse
import sys
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules"""


def main(sdk_path, test_path):
    """ Runs all tests at test_path

    :param sdk_path: Path to the GAE SDK installation
    :param test_path: Path to the tests to be run
    :return: None
    """
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.TestLoader().discover(test_path)
    unittest.TextTestRunner(verbosity = 2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        print('Error: Exactly 2 arguments required.')
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    main(SDK_PATH, TEST_PATH)