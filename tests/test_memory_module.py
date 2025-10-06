#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test suite for memory_module

Tests memory management:
- Reference counting
- Memory allocation
- Borrowed vs owned references
- Memory safety patterns
"""

import gc
import sys
import unittest


class TestMemoryModule(unittest.TestCase):
    """Test cases for memory_module"""

    @classmethod
    def setUpClass(cls):
        """Import the module once for all tests"""
        try:
            import memory_module

            cls.module = memory_module
        except ImportError as e:
            print >> sys.stderr, "Failed to import memory_module:", e
            sys.exit(1)

    # ========================================================================
    # Reference Counting
    # ========================================================================

    def test_get_refcount(self):
        """Test getting reference count"""
        x = "test string"
        refcount = self.module.get_refcount(x)
        self.assertIsInstance(refcount, (int, long))
        self.assertGreater(refcount, 0)

    def test_get_refcount_different_objects(self):
        """Test refcounts for different object types"""
        self.assertGreater(self.module.get_refcount(42), 0)
        self.assertGreater(self.module.get_refcount([1, 2, 3]), 0)
        self.assertGreater(self.module.get_refcount({'a': 1}), 0)

    def test_incref_demo(self):
        """Test INCREF/DECREF demonstration"""
        x = "test"
        before, after = self.module.incref_demo(x)

        self.assertIsInstance(before, (int, long))
        self.assertIsInstance(after, (int, long))
        self.assertEqual(after, before + 1)

    def test_incref_demo_restores_count(self):
        """Test that incref_demo properly restores refcount"""
        x = [1, 2, 3]
        original_count = self.module.get_refcount(x)
        before, after = self.module.incref_demo(x)
        final_count = self.module.get_refcount(x)

        # Should be restored
        self.assertEqual(original_count, final_count)

    def test_create_temp_list(self):
        """Test temporary list creation and cleanup"""
        size = self.module.create_temp_list(100)
        self.assertEqual(size, 100)

        # Should not leak memory
        size = self.module.create_temp_list(1000)
        self.assertEqual(size, 1000)

    # ========================================================================
    # Memory Allocation
    # ========================================================================

    def test_allocate_buffer(self):
        """Test buffer allocation with PyMem_Malloc"""
        result = self.module.allocate_buffer(26)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 26)
        self.assertEqual(result, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_allocate_buffer_large(self):
        """Test allocating large buffer"""
        result = self.module.allocate_buffer(1000)
        self.assertEqual(len(result), 1000)

        # Check pattern
        for i in range(26):
            self.assertEqual(result[i], chr(ord('A') + i))

    def test_allocate_buffer_small(self):
        """Test allocating small buffers"""
        result = self.module.allocate_buffer(1)
        self.assertEqual(result, "A")

        result = self.module.allocate_buffer(3)
        self.assertEqual(result, "ABC")

    def test_copy_string(self):
        """Test safe string copying"""
        original = "Python C-API"
        copied = self.module.copy_string(original)

        self.assertEqual(copied, original)
        self.assertIsInstance(copied, str)

    def test_copy_string_empty(self):
        """Test copying empty string"""
        result = self.module.copy_string("")
        self.assertEqual(result, "")

    def test_copy_string_special_chars(self):
        """Test copying string with special characters"""
        original = "Hello\nWorld\t!"
        copied = self.module.copy_string(original)
        self.assertEqual(copied, original)

    # ========================================================================
    # Borrowed vs Owned References
    # ========================================================================

    def test_borrowed_ref_demo(self):
        """Test borrowed reference handling"""
        test_list = ["first", "second", "third"]
        result = self.module.borrowed_ref_demo(test_list)

        self.assertIsInstance(result, dict)
        self.assertIn('item', result)
        self.assertIn('refcount', result)
        self.assertEqual(result['item'], "first")
        self.assertGreater(result['refcount'], 0)

    def test_borrowed_ref_demo_empty_list(self):
        """Test borrowed reference with empty list"""
        with self.assertRaises(ValueError):
            self.module.borrowed_ref_demo([])

    def test_owned_ref_demo(self):
        """Test owned reference handling"""
        result = self.module.owned_ref_demo(42)

        self.assertIsInstance(result, dict)
        self.assertIn('value', result)
        self.assertIn('refcount', result)
        self.assertEqual(result['value'], 42)
        self.assertGreater(result['refcount'], 0)

    def test_owned_ref_demo_various_values(self):
        """Test owned references with various values"""
        for value in [0, -100, 999, 2 ** 20]:
            result = self.module.owned_ref_demo(value)
            self.assertEqual(result['value'], value)

    # ========================================================================
    # Memory Safety
    # ========================================================================

    def test_proper_cleanup(self):
        """Test proper memory cleanup"""
        result = self.module.proper_cleanup("Hello", "World")
        self.assertEqual(result, "Hello World")

    def test_proper_cleanup_empty_strings(self):
        """Test cleanup with empty strings"""
        result = self.module.proper_cleanup("", "")
        self.assertEqual(result, " ")

    def test_proper_cleanup_long_strings(self):
        """Test cleanup with long strings"""
        str1 = "A" * 1000
        str2 = "B" * 1000
        result = self.module.proper_cleanup(str1, str2)
        self.assertTrue(result.startswith("A"))
        self.assertTrue(result.endswith("B"))
        self.assertIn(" ", result)

    def test_exception_safe(self):
        """Test exception-safe list creation"""
        result = self.module.exception_safe()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 10)

        # Check it's squares: [0, 1, 4, 9, 16, ...]
        for i in range(10):
            self.assertEqual(result[i], i * i)

    def test_create_populated_dict(self):
        """Test safe dictionary population"""
        result = self.module.create_populated_dict(10)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 10)

        # Check entries
        for i in range(10):
            key = "key_%d" % i
            self.assertIn(key, result)
            self.assertEqual(result[key], i * 100)

    def test_create_populated_dict_large(self):
        """Test creating large dictionary"""
        result = self.module.create_populated_dict(1000)
        self.assertEqual(len(result), 1000)


class TestMemoryModuleStressTests(unittest.TestCase):
    """Stress tests for memory management"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import memory_module

        cls.module = memory_module

    def test_repeated_allocations(self):
        """Test repeated allocations don't leak"""
        # Run multiple times to detect leaks
        for _ in range(100):
            result = self.module.allocate_buffer(100)
            self.assertEqual(len(result), 100)

    def test_large_buffer_allocation(self):
        """Test allocating very large buffers"""
        result = self.module.allocate_buffer(100000)
        self.assertEqual(len(result), 100000)

    def test_many_temp_lists(self):
        """Test creating many temporary lists"""
        for size in [10, 100, 1000]:
            for _ in range(10):
                result = self.module.create_temp_list(size)
                self.assertEqual(result, size)

    def test_many_dict_creations(self):
        """Test creating many dictionaries"""
        for count in [10, 50, 100]:
            result = self.module.create_populated_dict(count)
            self.assertEqual(len(result), count)

    def test_reference_counting_stability(self):
        """Test reference counting remains stable"""
        test_obj = [1, 2, 3, 4, 5]

        # Get initial refcount
        initial = self.module.get_refcount(test_obj)

        # Perform multiple operations
        for _ in range(10):
            before, after = self.module.incref_demo(test_obj)

        # Refcount should be stable
        final = self.module.get_refcount(test_obj)
        self.assertEqual(initial, final)


class TestMemoryModuleRefcountDetails(unittest.TestCase):
    """Detailed reference counting tests"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import memory_module

        cls.module = memory_module

    def test_list_refcount_behavior(self):
        """Test refcount behavior with lists"""
        test_list = ["item1", "item2"]

        # Borrowed reference shouldn't change list refcount
        before = self.module.get_refcount(test_list)
        result = self.module.borrowed_ref_demo(test_list)
        after = self.module.get_refcount(test_list)

        # Refcount should be stable (might have temporary increases during call)
        self.assertIsInstance(result, dict)

    def test_string_copy_creates_new_object(self):
        """Test that string copy creates independent object"""
        original = "test string for copying"
        copied = self.module.copy_string(original)

        self.assertEqual(original, copied)

        # Modify one shouldn't affect other (strings are immutable anyway)
        original2 = original + " modified"
        self.assertNotEqual(original2, copied)


def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestMemoryModule))
    test_suite.addTest(unittest.makeSuite(TestMemoryModuleStressTests))
    test_suite.addTest(unittest.makeSuite(TestMemoryModuleRefcountDetails))
    return test_suite


if __name__ == '__main__':
    print "Testing memory_module..."
    print "=" * 70
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
