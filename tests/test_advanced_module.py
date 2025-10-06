#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test suite for advanced_module

Tests advanced C-API topics:
- Callable objects
- Iterator protocol
- Capsules
- Module importing
- Unicode handling
"""

import sys
import unittest


class TestAdvancedModule(unittest.TestCase):
    """Test cases for advanced_module"""

    @classmethod
    def setUpClass(cls):
        """Import the module once for all tests"""
        try:
            import advanced_module

            cls.module = advanced_module
        except ImportError as e:
            print >> sys.stderr, "Failed to import advanced_module:", e
            sys.exit(1)

    # ========================================================================
    # Callable Objects
    # ========================================================================

    def test_call_function(self):
        """Test calling functions"""

        def add(a, b):
            return a + b

        result = self.module.call_function(add, (5, 3))
        self.assertEqual(result, 8)

    def test_call_function_builtin(self):
        """Test calling built-in functions"""
        result = self.module.call_function(len, ([1, 2, 3, 4, 5],))
        self.assertEqual(result, 5)

        result = self.module.call_function(sum, ([10, 20, 30],))
        self.assertEqual(result, 60)

    def test_call_function_not_callable(self):
        """Test calling non-callable object"""
        with self.assertRaises(TypeError):
            self.module.call_function(123, ())

        with self.assertRaises(TypeError):
            self.module.call_function("not callable", ())

    def test_call_with_kwargs(self):
        """Test calling with keyword arguments"""

        def greet(name, greeting="Hello"):
            return "%s, %s!" % (greeting, name)

        result = self.module.call_with_kwargs(greet, ("Alice",), {"greeting": "Hi"})
        self.assertEqual(result, "Hi, Alice!")

        result = self.module.call_with_kwargs(greet, ("Bob",), {})
        self.assertEqual(result, "Hello, Bob!")

    def test_call_method(self):
        """Test calling object methods"""
        test_list = [1, 2, 3]
        result = self.module.call_method(test_list, "append", 4)

        # Method returns None but modifies list
        self.assertIsNone(result)
        self.assertEqual(test_list, [1, 2, 3, 4])

    def test_call_method_with_return(self):
        """Test calling method that returns value"""
        test_list = [1, 2, 3]
        result = self.module.call_method(test_list, "pop", 0)
        self.assertEqual(result, 1)
        self.assertEqual(test_list, [2, 3])

    # ========================================================================
    # Iterator Protocol
    # ========================================================================

    def test_range_iterator_creation(self):
        """Test creating range iterator"""
        iterator = self.module.range_iterator(0, 5, 1)
        self.assertIsNotNone(iterator)

        # Check it's iterable
        result = list(iterator)
        self.assertEqual(result, [0, 1, 2, 3, 4])

    def test_range_iterator_with_step(self):
        """Test range iterator with step"""
        iterator = self.module.range_iterator(0, 10, 2)
        result = list(iterator)
        self.assertEqual(result, [0, 2, 4, 6, 8])

    def test_range_iterator_negative_step(self):
        """Test range iterator with negative step"""
        iterator = self.module.range_iterator(10, 0, -2)
        result = list(iterator)
        # Will produce values from 10 down
        self.assertTrue(len(result) == 0 or result[0] == 10)

    def test_range_iterator_empty(self):
        """Test range iterator that produces no values"""
        iterator = self.module.range_iterator(0, 0, 1)
        result = list(iterator)
        self.assertEqual(result, [])

    def test_range_iterator_manual_iteration(self):
        """Test manual iteration"""
        iterator = self.module.range_iterator(0, 3, 1)

        values = []
        for value in iterator:
            values.append(value)

        self.assertEqual(values, [0, 1, 2])

    def test_iterate_list(self):
        """Test iterating over list"""
        result = self.module.iterate([1, 2, 3, 4, 5])
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_iterate_string(self):
        """Test iterating over string"""
        result = self.module.iterate("hello")
        self.assertEqual(result, ['h', 'e', 'l', 'l', 'o'])

    def test_iterate_dict(self):
        """Test iterating over dictionary (keys)"""
        test_dict = {'a': 1, 'b': 2, 'c': 3}
        result = self.module.iterate(test_dict)

        # Should get keys
        self.assertEqual(set(result), {'a', 'b', 'c'})

    def test_iterate_tuple(self):
        """Test iterating over tuple"""
        result = self.module.iterate((10, 20, 30))
        self.assertEqual(result, [10, 20, 30])

    def test_iterate_set(self):
        """Test iterating over set"""
        test_set = {1, 2, 3}
        result = self.module.iterate(test_set)
        self.assertEqual(set(result), test_set)

    # ========================================================================
    # Capsules
    # ========================================================================

    def test_create_point_capsule(self):
        """Test creating point capsule"""
        point = self.module.create_point(10, 20, "Test Point")
        self.assertIsNotNone(point)

        # Should be a PyCapsule object
        self.assertTrue(str(type(point)).find("PyCapsule") >= 0)

    def test_get_point_data(self):
        """Test extracting data from point capsule"""
        point = self.module.create_point(100, 200, "Origin")
        data = self.module.get_point(point)

        self.assertIsInstance(data, dict)
        self.assertEqual(data['x'], 100)
        self.assertEqual(data['y'], 200)
        self.assertEqual(data['name'], "Origin")

    def test_point_capsule_multiple(self):
        """Test creating multiple point capsules"""
        point1 = self.module.create_point(0, 0, "P1")
        point2 = self.module.create_point(10, 10, "P2")

        data1 = self.module.get_point(point1)
        data2 = self.module.get_point(point2)

        self.assertEqual(data1['name'], "P1")
        self.assertEqual(data2['name'], "P2")
        self.assertNotEqual(data1['x'], data2['x'])

    def test_get_point_invalid_capsule(self):
        """Test getting point from non-capsule"""
        with self.assertRaises(TypeError):
            self.module.get_point("not a capsule")

        with self.assertRaises(TypeError):
            self.module.get_point(123)

    def test_point_with_long_name(self):
        """Test point with long name"""
        long_name = "A" * 100
        point = self.module.create_point(1, 2, long_name)
        data = self.module.get_point(point)

        # Name should be truncated to 49 chars (+ null terminator)
        self.assertLessEqual(len(data['name']), 50)

    # ========================================================================
    # Module Importing
    # ========================================================================

    def test_import_and_call_sys(self):
        """Test importing and calling sys module"""
        result = self.module.import_and_call("sys", "getdefaultencoding")
        self.assertIsInstance(result, str)

    def test_import_and_call_own_module(self):
        """Test importing our own modules"""
        # Try to import basics_module if available
        try:
            result = self.module.import_and_call("basics_module", "hello_world")
            self.assertIsInstance(result, str)
            self.assertIn("Hello", result)
        except ImportError:
            self.skipTest("basics_module not available")

    def test_import_nonexistent_module(self):
        """Test importing non-existent module"""
        with self.assertRaises(ImportError):
            self.module.import_and_call("nonexistent_module_xyz", "func")

    def test_import_nonexistent_function(self):
        """Test calling non-existent function"""
        with self.assertRaises(AttributeError):
            self.module.import_and_call("sys", "nonexistent_function_xyz")

    # ========================================================================
    # String Formatting
    # ========================================================================

    def test_format_string_with_tuple(self):
        """Test string formatting with tuple"""
        result = self.module.format_string("Hello, %s!", ("World",))
        self.assertEqual(result, "Hello, World!")

        result = self.module.format_string("%d + %d = %d", (5, 3, 8))
        self.assertEqual(result, "5 + 3 = 8")

    def test_format_string_with_dict(self):
        """Test string formatting with dictionary"""
        result = self.module.format_string(
            "%(name)s is %(age)d years old", {"name": "Alice", "age": 30}
        )
        self.assertEqual(result, "Alice is 30 years old")

    def test_format_string_multiple_values(self):
        """Test formatting with multiple values"""
        result = self.module.format_string(
            "%s: %d, %s: %d", ("apples", 5, "oranges", 3)
        )
        self.assertEqual(result, "apples: 5, oranges: 3")

    # ========================================================================
    # Unicode Handling
    # ========================================================================

    def test_str_to_unicode(self):
        """Test converting string to unicode"""
        result = self.module.str_to_unicode("Hello, World!")
        self.assertIsInstance(result, unicode)
        self.assertEqual(result, u"Hello, World!")

    def test_str_to_unicode_ascii(self):
        """Test converting ASCII string to unicode"""
        result = self.module.str_to_unicode("ASCII text 123")
        self.assertEqual(result, u"ASCII text 123")

    def test_str_to_unicode_utf8(self):
        """Test converting UTF-8 string to unicode"""
        utf8_str = "café"
        result = self.module.str_to_unicode(utf8_str)
        self.assertIsInstance(result, unicode)

    def test_unicode_to_str(self):
        """Test converting unicode to string"""
        result = self.module.unicode_to_str(u"Hello, World!")
        self.assertIsInstance(result, str)
        self.assertEqual(result, "Hello, World!")

    def test_unicode_roundtrip(self):
        """Test unicode conversion round-trip"""
        original = "Test string"
        unicode_ver = self.module.str_to_unicode(original)
        back_to_str = self.module.unicode_to_str(unicode_ver)

        self.assertEqual(original, back_to_str)

    def test_unicode_empty_string(self):
        """Test unicode conversion with empty string"""
        result = self.module.str_to_unicode("")
        self.assertEqual(result, u"")

        result = self.module.unicode_to_str(u"")
        self.assertEqual(result, "")


class TestAdvancedModuleEdgeCases(unittest.TestCase):
    """Test edge cases and complex scenarios"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import advanced_module

        cls.module = advanced_module

    def test_call_function_with_exception(self):
        """Test calling function that raises exception"""

        def failing_func():
            raise ValueError("test error")

        with self.assertRaises(ValueError):
            self.module.call_function(failing_func, ())

    def test_range_iterator_large_range(self):
        """Test iterator with large range"""
        iterator = self.module.range_iterator(0, 10000, 1)
        result = list(iterator)
        self.assertEqual(len(result), 10000)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-1], 9999)

    def test_iterate_empty_containers(self):
        """Test iterating over empty containers"""
        self.assertEqual(self.module.iterate([]), [])
        self.assertEqual(self.module.iterate(()), [])
        self.assertEqual(self.module.iterate(set()), [])
        self.assertEqual(self.module.iterate(""), [])

    def test_point_capsule_with_zeros(self):
        """Test point capsule with zero coordinates"""
        point = self.module.create_point(0, 0, "Origin")
        data = self.module.get_point(point)

        self.assertEqual(data['x'], 0)
        self.assertEqual(data['y'], 0)

    def test_point_capsule_with_negatives(self):
        """Test point capsule with negative coordinates"""
        point = self.module.create_point(-100, -200, "Negative")
        data = self.module.get_point(point)

        self.assertEqual(data['x'], -100)
        self.assertEqual(data['y'], -200)

    def test_format_string_special_chars(self):
        """Test string formatting with special characters"""
        result = self.module.format_string("Tab: %s, Newline: %s", ("\t", "\n"))
        self.assertIn("\t", result)
        self.assertIn("\n", result)


class TestAdvancedModuleIteratorDetails(unittest.TestCase):
    """Detailed tests for iterator protocol"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import advanced_module

        cls.module = advanced_module

    def test_range_iterator_type(self):
        """Test RangeIterator type"""
        iterator = self.module.range_iterator(0, 5, 1)

        # Should have __iter__ and next methods
        self.assertTrue(hasattr(iterator, '__iter__'))
        self.assertTrue(hasattr(iterator, 'next'))

    def test_range_iterator_reusable(self):
        """Test that iterator is not reusable after exhaustion"""
        iterator = self.module.range_iterator(0, 3, 1)

        # First iteration
        result1 = list(iterator)
        self.assertEqual(result1, [0, 1, 2])

        # Second iteration should be empty (iterator exhausted)
        result2 = list(iterator)
        self.assertEqual(result2, [])

    def test_iterate_generator(self):
        """Test iterating over generator"""

        def gen():
            yield 1
            yield 2
            yield 3

        result = self.module.iterate(gen())
        self.assertEqual(result, [1, 2, 3])


def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestAdvancedModule))
    test_suite.addTest(unittest.makeSuite(TestAdvancedModuleEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestAdvancedModuleIteratorDetails))
    return test_suite


if __name__ == '__main__':
    print "Testing advanced_module..."
    print "=" * 70
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
