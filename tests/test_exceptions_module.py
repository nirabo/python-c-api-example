#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test suite for exceptions_module

Tests exception handling:
- Raising standard exceptions
- Custom exceptions
- Exception checking and clearing
- Exception propagation
"""

import sys
import unittest
import warnings


class TestExceptionsModule(unittest.TestCase):
    """Test cases for exceptions_module"""

    @classmethod
    def setUpClass(cls):
        """Import the module once for all tests"""
        try:
            import exceptions_module

            cls.module = exceptions_module
        except ImportError as e:
            print >> sys.stderr, "Failed to import exceptions_module:", e
            sys.exit(1)

    # ========================================================================
    # Standard Exceptions
    # ========================================================================

    def test_raise_value_error(self):
        """Test raising ValueError"""
        with self.assertRaises(ValueError) as cm:
            self.module.raise_value_error("custom message")

        self.assertIn("custom message", str(cm.exception))

    def test_raise_type_error(self):
        """Test raising TypeError"""
        with self.assertRaises(TypeError) as cm:
            self.module.raise_type_error()

        self.assertIn("TypeError", str(cm.exception))

    def test_raise_runtime_error(self):
        """Test raising RuntimeError with formatted message"""
        with self.assertRaises(RuntimeError) as cm:
            self.module.raise_runtime_error()

        exception_msg = str(cm.exception)
        self.assertIn("Runtime error", exception_msg)
        self.assertIn("42", exception_msg)

    def test_raise_index_error(self):
        """Test raising IndexError"""
        with self.assertRaises(IndexError) as cm:
            self.module.raise_index_error(99)

        self.assertIn("99", str(cm.exception))
        self.assertIn("out of range", str(cm.exception))

    # ========================================================================
    # Custom Exceptions
    # ========================================================================

    def test_custom_error_exists(self):
        """Test that custom exception class exists"""
        self.assertTrue(hasattr(self.module, 'CustomError'))
        self.assertTrue(issubclass(self.module.CustomError, Exception))

    def test_validation_error_exists(self):
        """Test that ValidationError class exists"""
        self.assertTrue(hasattr(self.module, 'ValidationError'))
        self.assertTrue(issubclass(self.module.ValidationError, Exception))

    def test_raise_custom_error(self):
        """Test raising custom exception"""
        with self.assertRaises(self.module.CustomError) as cm:
            self.module.raise_custom_error("custom error occurred")

        self.assertIn("custom error occurred", str(cm.exception))

    def test_raise_validation_error(self):
        """Test raising ValidationError"""
        with self.assertRaises(self.module.ValidationError) as cm:
            self.module.raise_validation_error("email", "invalid format")

        exception_msg = str(cm.exception)
        self.assertIn("email", exception_msg)
        self.assertIn("invalid format", exception_msg)

    def test_custom_exception_catchable(self):
        """Test that custom exceptions can be caught"""
        try:
            self.module.raise_custom_error("test")
            self.fail("Should have raised CustomError")
        except self.module.CustomError:
            pass  # Expected

    # ========================================================================
    # Exception Checking and Clearing
    # ========================================================================

    def test_check_and_clear_with_exception(self):
        """Test checking and clearing exceptions"""

        def failing_func():
            raise ValueError("test error")

        result = self.module.check_and_clear(failing_func)
        self.assertIsInstance(result, str)
        self.assertIn("caught and cleared", result.lower())

    def test_check_and_clear_no_exception(self):
        """Test check and clear with no exception"""

        def working_func():
            return "success"

        result = self.module.check_and_clear(working_func)
        self.assertIsInstance(result, str)
        self.assertIn("No exception", result)

    def test_check_exception_type_value_error(self):
        """Test identifying ValueError"""

        def raise_value():
            raise ValueError("test")

        result = self.module.check_exception_type(raise_value)
        self.assertIn("ValueError", result)

    def test_check_exception_type_type_error(self):
        """Test identifying TypeError"""

        def raise_type():
            raise TypeError("test")

        result = self.module.check_exception_type(raise_type)
        self.assertIn("TypeError", result)

    def test_check_exception_type_other(self):
        """Test identifying other exceptions"""

        def raise_other():
            raise RuntimeError("test")

        result = self.module.check_exception_type(raise_other)
        self.assertIn("Other", result)

    def test_check_exception_type_no_exception(self):
        """Test with no exception"""

        def no_error():
            return "ok"

        result = self.module.check_exception_type(no_error)
        self.assertIn("No exception", result)

    # ========================================================================
    # Exception Information
    # ========================================================================

    def test_get_exception_info(self):
        """Test getting exception information"""

        def failing_func():
            raise ValueError("detailed error message")

        result = self.module.get_exception_info(failing_func)
        self.assertIsInstance(result, dict)
        self.assertIn('type', result)
        self.assertIn('value', result)
        self.assertIn('has_traceback', result)

        # Check content
        self.assertIn("ValueError", result['type'])
        self.assertIn("detailed error message", result['value'])

    def test_get_exception_info_no_exception(self):
        """Test getting info when no exception occurs"""

        def working_func():
            return "success"

        result = self.module.get_exception_info(working_func)
        self.assertIsNone(result)

    # ========================================================================
    # Exception Propagation
    # ========================================================================

    def test_safe_divide(self):
        """Test safe division"""
        result = self.module.safe_divide(10.0, 2.0)
        self.assertAlmostEqual(result, 5.0)

        result = self.module.safe_divide(100.0, 4.0)
        self.assertAlmostEqual(result, 25.0)

    def test_safe_divide_zero(self):
        """Test safe division by zero"""
        with self.assertRaises(ZeroDivisionError):
            self.module.safe_divide(10.0, 0.0)

    def test_safe_divide_negative(self):
        """Test safe division with negative numbers"""
        result = self.module.safe_divide(-10.0, 2.0)
        self.assertAlmostEqual(result, -5.0)

    def test_nested_call_demo(self):
        """Test exception propagation through nested calls"""
        with self.assertRaises(ZeroDivisionError):
            self.module.nested_call_demo()

    # ========================================================================
    # Error Indicators
    # ========================================================================

    def test_check_error_occurred(self):
        """Test checking if error occurred"""
        # Should be False (no error pending)
        result = self.module.check_error_occurred()
        self.assertFalse(result)

    def test_set_and_check(self):
        """Test setting error and checking"""
        with self.assertRaises(RuntimeError):
            self.module.set_and_check()

    # ========================================================================
    # Warnings
    # ========================================================================

    def test_issue_warning(self):
        """Test issuing deprecation warning"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            result = self.module.issue_warning("This is deprecated")

            # Should return None
            self.assertIsNone(result)

            # Should have issued a warning
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("deprecated", str(w[0].message))


class TestExceptionsModuleEdgeCases(unittest.TestCase):
    """Test edge cases and complex scenarios"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import exceptions_module

        cls.module = exceptions_module

    def test_exception_with_empty_message(self):
        """Test raising exception with empty message"""
        with self.assertRaises(ValueError):
            self.module.raise_value_error("")

    def test_exception_with_long_message(self):
        """Test exception with very long message"""
        long_msg = "A" * 10000
        with self.assertRaises(ValueError) as cm:
            self.module.raise_value_error(long_msg)

        self.assertIn("A", str(cm.exception))

    def test_exception_with_special_chars(self):
        """Test exception message with special characters"""
        msg = "Error: \n\t<>&'\""
        with self.assertRaises(ValueError) as cm:
            self.module.raise_value_error(msg)

        self.assertIn("Error", str(cm.exception))

    def test_multiple_exception_clears(self):
        """Test clearing multiple exceptions"""

        def failing():
            raise ValueError("test")

        for _ in range(10):
            result = self.module.check_and_clear(failing)
            self.assertIn("cleared", result.lower())

    def test_nested_exception_types(self):
        """Test with different exception types in sequence"""

        def raise_value():
            raise ValueError("v")

        def raise_type():
            raise TypeError("t")

        result1 = self.module.check_exception_type(raise_value)
        self.assertIn("ValueError", result1)

        result2 = self.module.check_exception_type(raise_type)
        self.assertIn("TypeError", result2)


class TestExceptionsModuleCustomExceptions(unittest.TestCase):
    """Test custom exception behavior in detail"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import exceptions_module

        cls.module = exceptions_module

    def test_custom_error_hierarchy(self):
        """Test custom exception hierarchy"""
        # Should be catchable as Exception
        with self.assertRaises(Exception):
            self.module.raise_custom_error("test")

        # Should be catchable as CustomError
        with self.assertRaises(self.module.CustomError):
            self.module.raise_custom_error("test")

    def test_validation_error_hierarchy(self):
        """Test ValidationError hierarchy"""
        with self.assertRaises(Exception):
            self.module.raise_validation_error("field", "reason")

        with self.assertRaises(self.module.ValidationError):
            self.module.raise_validation_error("field", "reason")

    def test_multiple_validation_errors(self):
        """Test raising multiple validation errors"""
        fields = ["email", "password", "username"]
        reasons = ["invalid", "too short", "taken"]

        for field, reason in zip(fields, reasons):
            with self.assertRaises(self.module.ValidationError) as cm:
                self.module.raise_validation_error(field, reason)

            msg = str(cm.exception)
            self.assertIn(field, msg)
            self.assertIn(reason, msg)

    def test_custom_exceptions_are_different(self):
        """Test that custom exceptions are distinct types"""
        self.assertIsNot(self.module.CustomError, self.module.ValidationError)
        self.assertNotEqual(self.module.CustomError, self.module.ValidationError)


class TestExceptionsModuleArguments(unittest.TestCase):
    """Test argument handling in exception functions"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import exceptions_module

        cls.module = exceptions_module

    def test_raise_value_error_wrong_args(self):
        """Test ValueError raising with wrong arguments"""
        with self.assertRaises(TypeError):
            self.module.raise_value_error()  # Missing argument

        with self.assertRaises(TypeError):
            self.module.raise_value_error(123)  # Wrong type

    def test_safe_divide_wrong_args(self):
        """Test safe_divide with wrong arguments"""
        with self.assertRaises(TypeError):
            self.module.safe_divide(10.0)  # Missing argument

        with self.assertRaises(TypeError):
            self.module.safe_divide()  # No arguments


def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestExceptionsModule))
    test_suite.addTest(unittest.makeSuite(TestExceptionsModuleEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestExceptionsModuleCustomExceptions))
    test_suite.addTest(unittest.makeSuite(TestExceptionsModuleArguments))
    return test_suite


if __name__ == '__main__':
    print "Testing exceptions_module..."
    print "=" * 70
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
