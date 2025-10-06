#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test suite for basics_module

Tests fundamental C-API concepts:
- Argument parsing
- Return value building
- Type conversions
- Optional arguments
- Multiple return values
"""

import sys
import unittest


class TestBasicsModule(unittest.TestCase):
    """Test cases for basics_module"""

    @classmethod
    def setUpClass(cls):
        """Import the module once for all tests"""
        try:
            import basics_module

            cls.module = basics_module
        except ImportError as e:
            print >> sys.stderr, "Failed to import basics_module:", e
            print >> sys.stderr, "Make sure to build with: python setup.py build_ext --inplace"
            sys.exit(1)

    def test_module_constants(self):
        """Test module-level constants"""
        self.assertEqual(self.module.VERSION_MAJOR, 1)
        self.assertEqual(self.module.VERSION_MINOR, 0)
        self.assertEqual(self.module.AUTHOR, "C-API Tutorial")

    def test_hello_world(self):
        """Test simple string return"""
        result = self.module.hello_world()
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello from C extension!")

    def test_greet_name(self):
        """Test string argument parsing"""
        self.assertIn("Alice", self.module.greet_name("Alice"))
        self.assertIn("Bob", self.module.greet_name("Bob"))
        self.assertIn("", self.module.greet_name(""))

    def test_greet_name_invalid_args(self):
        """Test error handling for invalid arguments"""
        with self.assertRaises(TypeError):
            self.module.greet_name()  # Missing argument
        with self.assertRaises(TypeError):
            self.module.greet_name(123)  # Wrong type
        with self.assertRaises(TypeError):
            self.module.greet_name("a", "b")  # Too many arguments

    def test_add_numbers(self):
        """Test integer addition"""
        self.assertEqual(self.module.add_numbers(5, 3), 8)
        self.assertEqual(self.module.add_numbers(100, 200), 300)
        self.assertEqual(self.module.add_numbers(-10, 25), 15)
        self.assertEqual(self.module.add_numbers(0, 0), 0)
        self.assertEqual(self.module.add_numbers(-5, -3), -8)

    def test_add_numbers_large_values(self):
        """Test with large integers - demonstrates C int overflow behavior"""
        large = 2**30
        result = self.module.add_numbers(large, large)
        # C int overflow: 2^31 overflows to -2^31 due to 32-bit signed integer limits
        # This test documents the expected overflow behavior
        self.assertEqual(result, -2147483648)

    def test_multiply_floats(self):
        """Test float multiplication"""
        self.assertAlmostEqual(self.module.multiply_floats(3.14, 2.0), 6.28)
        self.assertAlmostEqual(self.module.multiply_floats(7.5, 4.2), 31.5)
        self.assertAlmostEqual(self.module.multiply_floats(-2.5, 3.0), -7.5)
        self.assertEqual(self.module.multiply_floats(0.0, 100.0), 0.0)

    def test_divide_safe(self):
        """Test safe division"""
        self.assertAlmostEqual(self.module.divide_safe(10.0, 3.0), 10.0 / 3.0)
        self.assertAlmostEqual(self.module.divide_safe(100.0, 4.0), 25.0)
        self.assertAlmostEqual(self.module.divide_safe(-10.0, 2.0), -5.0)

    def test_divide_by_zero(self):
        """Test division by zero error handling"""
        with self.assertRaises(ZeroDivisionError):
            self.module.divide_safe(10.0, 0.0)
        with self.assertRaises(ZeroDivisionError):
            self.module.divide_safe(0.0, 0.0)

    def test_is_even(self):
        """Test boolean return values"""
        self.assertTrue(self.module.is_even(4))
        self.assertTrue(self.module.is_even(0))
        self.assertTrue(self.module.is_even(-2))
        self.assertTrue(self.module.is_even(1000))

        self.assertFalse(self.module.is_even(7))
        self.assertFalse(self.module.is_even(1))
        self.assertFalse(self.module.is_even(-3))
        self.assertFalse(self.module.is_even(999))

    def test_string_length(self):
        """Test string length calculation"""
        self.assertEqual(self.module.string_length("hello"), 5)
        self.assertEqual(self.module.string_length("Python C-API"), 12)
        self.assertEqual(self.module.string_length(""), 0)
        self.assertEqual(self.module.string_length("a"), 1)

    def test_string_length_unicode(self):
        """Test string length with special characters"""
        # In Python 2.7, encoded UTF-8 strings
        test_str = "café"
        result = self.module.string_length(test_str)
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_power_default_exponent(self):
        """Test power function with default exponent"""
        self.assertAlmostEqual(self.module.power(2.0), 4.0)
        self.assertAlmostEqual(self.module.power(5.0), 25.0)
        self.assertAlmostEqual(self.module.power(10.0), 100.0)
        self.assertAlmostEqual(self.module.power(1.0), 1.0)
        self.assertAlmostEqual(self.module.power(0.0), 0.0)

    def test_power_custom_exponent(self):
        """Test power function with custom exponent"""
        self.assertAlmostEqual(self.module.power(2.0, 3.0), 8.0)
        self.assertAlmostEqual(self.module.power(3.0, 4.0), 81.0)
        self.assertAlmostEqual(self.module.power(10.0, 0.5), 3.162277660168, places=5)
        self.assertAlmostEqual(self.module.power(2.0, 0.0), 1.0)

    def test_power_keyword_args(self):
        """Test power function with keyword arguments"""
        self.assertAlmostEqual(self.module.power(base=2.0, exponent=3.0), 8.0)
        self.assertAlmostEqual(self.module.power(exponent=2.0, base=5.0), 25.0)
        self.assertAlmostEqual(self.module.power(base=3.0), 9.0)

    def test_divmod(self):
        """Test divmod returning tuple"""
        quotient, remainder = self.module.divmod(17, 5)
        self.assertEqual(quotient, 3)
        self.assertEqual(remainder, 2)

        q, r = self.module.divmod(100, 7)
        self.assertEqual(q, 14)
        self.assertEqual(r, 2)

        q, r = self.module.divmod(50, 10)
        self.assertEqual(q, 5)
        self.assertEqual(r, 0)

    def test_divmod_negative(self):
        """Test divmod with negative numbers"""
        q, r = self.module.divmod(-17, 5)
        self.assertEqual(q, -3)
        self.assertEqual(r, -2)  # C division behavior

    def test_divmod_zero_divisor(self):
        """Test divmod with zero divisor"""
        with self.assertRaises(ZeroDivisionError):
            self.module.divmod(10, 0)

    def test_get_statistics(self):
        """Test dictionary return value"""
        stats = self.module.get_statistics(5.0)
        self.assertIsInstance(stats, dict)
        self.assertIn('value', stats)
        self.assertIn('square', stats)
        self.assertIn('cube', stats)

        self.assertAlmostEqual(stats['value'], 5.0)
        self.assertAlmostEqual(stats['square'], 25.0)
        self.assertAlmostEqual(stats['cube'], 125.0)

    def test_get_statistics_zero(self):
        """Test statistics with zero"""
        stats = self.module.get_statistics(0.0)
        self.assertEqual(stats['value'], 0.0)
        self.assertEqual(stats['square'], 0.0)
        self.assertEqual(stats['cube'], 0.0)

    def test_get_statistics_negative(self):
        """Test statistics with negative number"""
        stats = self.module.get_statistics(-3.0)
        self.assertAlmostEqual(stats['value'], -3.0)
        self.assertAlmostEqual(stats['square'], 9.0)
        self.assertAlmostEqual(stats['cube'], -27.0)

    def test_return_none(self):
        """Test None return value"""
        result = self.module.return_none()
        self.assertIsNone(result)

    def test_accept_optional_no_arg(self):
        """Test optional argument with no argument provided"""
        result = self.module.accept_optional()
        self.assertIsInstance(result, str)
        self.assertIn("No argument", result)

    def test_accept_optional_none(self):
        """Test optional argument with explicit None"""
        result = self.module.accept_optional(None)
        self.assertIsInstance(result, str)
        self.assertIn("No argument", result)

    def test_accept_optional_with_value(self):
        """Test optional argument with various values"""
        result = self.module.accept_optional(42)
        self.assertIsInstance(result, str)
        self.assertIn("42", result)

        result = self.module.accept_optional("test")
        self.assertIsInstance(result, str)
        self.assertIn("test", result)

        result = self.module.accept_optional([1, 2, 3])
        self.assertIsInstance(result, str)


class TestBasicsModuleEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import basics_module

        cls.module = basics_module

    def test_overflow_protection(self):
        """Test behavior with very large numbers"""
        # Python 2.7 int overflow behavior
        large = sys.maxint
        try:
            result = self.module.add_numbers(large, 1)
            # Should handle or overflow
            self.assertIsInstance(result, (int, long))
        except (OverflowError, ValueError):
            pass  # Acceptable behavior

    def test_float_special_values(self):
        """Test with special float values"""
        import math

        # Infinity
        result = self.module.multiply_floats(float('inf'), 2.0)
        self.assertTrue(math.isinf(result))

        # NaN
        result = self.module.multiply_floats(float('nan'), 2.0)
        self.assertTrue(math.isnan(result))

    def test_very_long_string(self):
        """Test with very long strings"""
        long_str = "a" * 10000
        result = self.module.string_length(long_str)
        self.assertEqual(result, 10000)

        result = self.module.greet_name(long_str)
        self.assertIn(long_str, result)


def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestBasicsModule))
    test_suite.addTest(unittest.makeSuite(TestBasicsModuleEdgeCases))
    return test_suite


if __name__ == '__main__':
    print "Testing basics_module..."
    print "=" * 70
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
