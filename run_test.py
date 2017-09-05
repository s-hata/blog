import unittest
import argparse
import shutil

from coverage import coverage

from test.user_test import UserTestCase


cov = coverage(config_file=True)
cov.start()

def clean():
    shutil.rmtree('reports/coverage')

if __name__ == "__main__":
    clean()
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'type',
        help='The test type[ut|fn].')

    args = parser.parse_args()

    if args.type == 'ut':
        ut = unittest.TestLoader().loadTestsFromTestCase(UserTestCase)
        unittest.TextTestRunner(verbosity=2).run(ut)

    if args.type == 'fn':
        #fn  = unittest.TestLoader().loadTestsFromTestCase(TodoResourceTestCase)
        #unittest.TextTestRunner(verbosity=2).run(fn)
        pass

    cov.stop()
    cov.save()
    print('\n\nCoverage Report:\n')
    cov.report()
    print('HTML version: ' + 'reports/coverage/index.html')
    cov.html_report(directory='reports/coverage')
    cov.erase()
