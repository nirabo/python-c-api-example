#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Comprehensive test runner for all C-API tutorial modules

Runs all test suites and provides detailed coverage report.
"""

import os
import sys
import unittest

# Add parent directory to path for module imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def discover_tests():
    """Discover all test modules"""
    test_modules = [
        'test_basics_module',
        'test_objects_module',
        'test_memory_module',
        'test_exceptions_module',
        'test_advanced_module',
    ]

    suites = []
    failed_imports = []

    for module_name in test_modules:
        try:
            module = __import__(module_name)
            if hasattr(module, 'suite'):
                suites.append(module.suite())
            else:
                loader = unittest.TestLoader()
                suites.append(loader.loadTestsFromModule(module))
        except ImportError as e:
            failed_imports.append((module_name, str(e)))

    return suites, failed_imports


def print_header(text, char='='):
    """Print formatted header"""
    print ""
    print char * 78
    print text.center(78)
    print char * 78
    print ""


def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY", "=")

    total_tests = results.testsRun
    failures = len(results.failures)
    errors = len(results.errors)
    skipped = len(results.skipped) if hasattr(results, 'skipped') else 0

    print "Total Tests:    %d" % total_tests
    print "Passed:         %d" % (total_tests - failures - errors - skipped)
    print "Failed:         %d" % failures
    print "Errors:         %d" % errors
    print "Skipped:        %d" % skipped
    print ""

    if failures > 0:
        print "FAILURES:"
        print "-" * 78
        for test, traceback in results.failures:
            print "  * %s" % test
        print ""

    if errors > 0:
        print "ERRORS:"
        print "-" * 78
        for test, traceback in results.errors:
            print "  * %s" % test
        print ""

    success_rate = (
        100.0 * (total_tests - failures - errors) / total_tests
        if total_tests > 0
        else 0
    )
    print "Success Rate: %.1f%%" % success_rate
    print ""


def main():
    """Main test runner"""
    print_header("Python 2.7 C-API Tutorial - Test Suite", "=")

    # Check if modules are built
    print "Checking if C extension modules are built..."
    modules_to_check = [
        'basics_module',
        'objects_module',
        'memory_module',
        'exceptions_module',
        'advanced_module',
    ]

    missing_modules = []
    for module_name in modules_to_check:
        try:
            __import__(module_name)
            print "  [OK] %s" % module_name
        except ImportError:
            print "  [MISSING] %s" % module_name
            missing_modules.append(module_name)

    if missing_modules:
        print ""
        print "ERROR: Some modules are not built!"
        print "Please build the modules first:"
        print "  python setup.py build_ext --inplace"
        print ""
        print "Or in Docker:"
        print "  make dev"
        print ""
        return 1

    print ""
    print "All modules found. Discovering tests..."
    print ""

    # Discover and load tests
    suites, failed_imports = discover_tests()

    if failed_imports:
        print "WARNING: Failed to import some test modules:"
        for module_name, error in failed_imports:
            print "  * %s: %s" % (module_name, error)
        print ""

    if not suites:
        print "ERROR: No test suites found!"
        return 1

    # Combine all test suites
    master_suite = unittest.TestSuite(suites)

    # Run tests
    print_header("Running Tests", "-")
    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(master_suite)

    # Print summary
    print_summary(results)

    # Return exit code
    if results.wasSuccessful():
        print_header("ALL TESTS PASSED!", "=")
        return 0
    else:
        print_header("SOME TESTS FAILED", "=")
        return 1


if __name__ == '__main__':
    sys.exit(main())
