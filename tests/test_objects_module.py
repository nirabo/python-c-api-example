#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
"""
Test suite for objects_module

Tests object manipulation:
- List operations
- Dictionary operations
- Tuple and set operations
- Attribute access
- Type checking
"""

import sys
import unittest


class TestObjectsModule(unittest.TestCase):
    """Test cases for objects_module"""

    @classmethod
    def setUpClass(cls):
        """Import the module once for all tests"""
        try:
            import objects_module

            cls.module = objects_module
        except ImportError as e:
            print >> sys.stderr, "Failed to import objects_module:", e
            sys.exit(1)

    # ========================================================================
    # List Operations
    # ========================================================================

    def test_create_list(self):
        """Test list creation with squares"""
        result = self.module.create_list(5)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 5)
        self.assertEqual(result, [0, 1, 4, 9, 16])

    def test_create_list_empty(self):
        """Test creating empty list"""
        result = self.module.create_list(0)
        self.assertEqual(result, [])

    def test_create_list_large(self):
        """Test creating large list"""
        result = self.module.create_list(100)
        self.assertEqual(len(result), 100)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[10], 100)
        self.assertEqual(result[99], 99 * 99)

    def test_sum_list(self):
        """Test summing list elements"""
        self.assertEqual(self.module.sum_list([1, 2, 3, 4, 5]), 15)
        self.assertEqual(self.module.sum_list([10, 20, 30]), 60)
        self.assertEqual(self.module.sum_list([0, 0, 0]), 0)
        self.assertEqual(self.module.sum_list([-5, 5]), 0)

    def test_sum_list_empty(self):
        """Test summing empty list"""
        self.assertEqual(self.module.sum_list([]), 0)

    def test_sum_list_invalid_type(self):
        """Test sum_list with non-integers"""
        with self.assertRaises(TypeError):
            self.module.sum_list([1, 2, "three"])

        with self.assertRaises(TypeError):
            self.module.sum_list([1.5, 2.5])

    def test_sum_list_wrong_argument(self):
        """Test sum_list with wrong argument type"""
        with self.assertRaises(TypeError):
            self.module.sum_list("not a list")

        with self.assertRaises(TypeError):
            self.module.sum_list(123)

    def test_reverse_list(self):
        """Test list reversal"""
        test_list = [1, 2, 3, 4, 5]
        result = self.module.reverse_list(test_list)

        # Check in-place reversal
        self.assertEqual(test_list, [5, 4, 3, 2, 1])
        # Check returned list is same object
        self.assertIs(result, test_list)

    def test_reverse_list_empty(self):
        """Test reversing empty list"""
        test_list = []
        result = self.module.reverse_list(test_list)
        self.assertEqual(result, [])

    # ========================================================================
    # Dictionary Operations
    # ========================================================================

    def test_create_dict(self):
        """Test dictionary creation"""
        result = self.module.create_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 5)
        self.assertEqual(result['key0'], 0)
        self.assertEqual(result['key1'], 10)
        self.assertEqual(result['key4'], 40)

    def test_dict_has_key(self):
        """Test dictionary key checking"""
        test_dict = {'a': 1, 'b': 2, 'c': 3}
        self.assertTrue(self.module.dict_has_key(test_dict, 'a'))
        self.assertTrue(self.module.dict_has_key(test_dict, 'b'))
        self.assertFalse(self.module.dict_has_key(test_dict, 'z'))
        self.assertFalse(self.module.dict_has_key(test_dict, ''))

    def test_dict_has_key_empty_dict(self):
        """Test key checking on empty dictionary"""
        self.assertFalse(self.module.dict_has_key({}, 'any'))

    def test_merge_dicts(self):
        """Test dictionary merging"""
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'c': 3, 'd': 4}
        result = self.module.merge_dicts(dict1, dict2)

        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 4)
        self.assertEqual(result['a'], 1)
        self.assertEqual(result['b'], 2)
        self.assertEqual(result['c'], 3)
        self.assertEqual(result['d'], 4)

    def test_merge_dicts_overlapping_keys(self):
        """Test merging dicts with overlapping keys"""
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'b': 20, 'c': 3}
        result = self.module.merge_dicts(dict1, dict2)

        # dict2 values should override
        self.assertEqual(result['a'], 1)
        self.assertEqual(result['b'], 20)
        self.assertEqual(result['c'], 3)

    def test_merge_dicts_empty(self):
        """Test merging empty dictionaries"""
        result = self.module.merge_dicts({}, {})
        self.assertEqual(result, {})

        result = self.module.merge_dicts({'a': 1}, {})
        self.assertEqual(result, {'a': 1})

    # ========================================================================
    # Tuple Operations
    # ========================================================================

    def test_create_tuple(self):
        """Test tuple creation"""
        result = self.module.create_tuple(5)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 5)
        self.assertEqual(result, (1, 2, 3, 4, 5))

    def test_create_tuple_size_one(self):
        """Test creating single-element tuple"""
        result = self.module.create_tuple(1)
        self.assertEqual(result, (1,))

    def test_tuple_element(self):
        """Test tuple element access"""
        test_tuple = (10, 20, 30, 40, 50)
        self.assertEqual(self.module.tuple_element(test_tuple, 0), 10)
        self.assertEqual(self.module.tuple_element(test_tuple, 2), 30)
        self.assertEqual(self.module.tuple_element(test_tuple, 4), 50)

    def test_tuple_element_out_of_range(self):
        """Test tuple element access with invalid index"""
        test_tuple = (1, 2, 3)
        with self.assertRaises(IndexError):
            self.module.tuple_element(test_tuple, 5)

        with self.assertRaises(IndexError):
            self.module.tuple_element(test_tuple, -1)

    # ========================================================================
    # Set Operations
    # ========================================================================

    def test_create_set(self):
        """Test set creation from list"""
        result = self.module.create_set([1, 2, 2, 3, 3, 3, 4])
        self.assertIsInstance(result, set)
        self.assertEqual(result, {1, 2, 3, 4})

    def test_create_set_duplicates(self):
        """Test that set removes duplicates"""
        result = self.module.create_set([1, 1, 1, 1])
        self.assertEqual(result, {1})

    def test_set_union(self):
        """Test set union operation"""
        set1 = {1, 2, 3}
        set2 = {3, 4, 5}
        result = self.module.set_union(set1, set2)

        self.assertIsInstance(result, set)
        self.assertEqual(result, {1, 2, 3, 4, 5})

    def test_set_union_disjoint(self):
        """Test union of disjoint sets"""
        set1 = {1, 2}
        set2 = {3, 4}
        result = self.module.set_union(set1, set2)
        self.assertEqual(result, {1, 2, 3, 4})

    # ========================================================================
    # Attribute Access
    # ========================================================================

    def test_get_attr(self):
        """Test getting object attributes"""

        class TestObj(object):
            def __init__(self):
                self.name = "test"
                self.value = 42

        obj = TestObj()
        self.assertEqual(self.module.get_attr(obj, "name"), "test")
        self.assertEqual(self.module.get_attr(obj, "value"), 42)

    def test_get_attr_nonexistent(self):
        """Test getting nonexistent attribute"""

        class TestObj(object):
            pass

        obj = TestObj()
        result = self.module.get_attr(obj, "nonexistent")
        self.assertIsNone(result)

    def test_set_attr(self):
        """Test setting object attributes"""

        class TestObj(object):
            pass

        obj = TestObj()
        result = self.module.set_attr(obj, "new_attr", "value")
        self.assertIsNone(result)
        self.assertEqual(obj.new_attr, "value")

    def test_set_attr_existing(self):
        """Test overwriting existing attribute"""

        class TestObj(object):
            def __init__(self):
                self.attr = "old"

        obj = TestObj()
        self.module.set_attr(obj, "attr", "new")
        self.assertEqual(obj.attr, "new")

    def test_has_attr(self):
        """Test checking for attribute existence"""

        class TestObj(object):
            def __init__(self):
                self.exists = True

        obj = TestObj()
        self.assertTrue(self.module.has_attr(obj, "exists"))
        self.assertFalse(self.module.has_attr(obj, "missing"))

    # ========================================================================
    # Type Checking
    # ========================================================================

    def test_get_type(self):
        """Test getting type name"""
        self.assertEqual(self.module.get_type(42), "int")
        self.assertEqual(self.module.get_type("hello"), "str")
        self.assertEqual(self.module.get_type([1, 2, 3]), "list")
        self.assertEqual(self.module.get_type({'a': 1}), "dict")
        self.assertEqual(self.module.get_type((1, 2)), "tuple")
        self.assertEqual(self.module.get_type({1, 2}), "set")

    def test_check_type_int(self):
        """Test type checking for integer"""
        result = self.module.check_type(42)
        self.assertTrue(result['is_int'])
        self.assertFalse(result['is_string'])
        self.assertFalse(result['is_list'])

    def test_check_type_string(self):
        """Test type checking for string"""
        result = self.module.check_type("hello")
        self.assertTrue(result['is_string'])
        self.assertFalse(result['is_int'])
        self.assertFalse(result['is_list'])

    def test_check_type_list(self):
        """Test type checking for list"""
        result = self.module.check_type([1, 2, 3])
        self.assertTrue(result['is_list'])
        self.assertFalse(result['is_dict'])
        self.assertFalse(result['is_tuple'])

    def test_check_type_dict(self):
        """Test type checking for dictionary"""
        result = self.module.check_type({'a': 1})
        self.assertTrue(result['is_dict'])
        self.assertFalse(result['is_list'])

    def test_check_type_unicode(self):
        """Test type checking for unicode"""
        result = self.module.check_type(u"hello")
        self.assertTrue(result['is_unicode'])
        self.assertFalse(result['is_string'])

    # ========================================================================
    # Object Comparison
    # ========================================================================

    def test_compare_integers(self):
        """Test comparing integers"""
        self.assertEqual(self.module.compare(5, 10), -1)  # 5 < 10
        self.assertEqual(self.module.compare(10, 5), 1)  # 10 > 5
        self.assertEqual(self.module.compare(5, 5), 0)  # 5 == 5

    def test_compare_strings(self):
        """Test comparing strings"""
        self.assertEqual(self.module.compare("abc", "xyz"), -1)
        self.assertEqual(self.module.compare("xyz", "abc"), 1)
        self.assertEqual(self.module.compare("same", "same"), 0)

    def test_compare_lists(self):
        """Test comparing lists"""
        self.assertEqual(self.module.compare([1, 2], [1, 3]), -1)
        self.assertEqual(self.module.compare([1, 3], [1, 2]), 1)
        self.assertEqual(self.module.compare([1, 2], [1, 2]), 0)


class TestObjectsModuleEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions"""

    @classmethod
    def setUpClass(cls):
        """Import the module"""
        import objects_module

        cls.module = objects_module

    def test_large_list(self):
        """Test with large lists"""
        large_list = range(10000)
        total = self.module.sum_list(large_list)
        self.assertEqual(total, sum(large_list))

    def test_deep_nesting(self):
        """Test with deeply nested structures"""
        nested_dict = {'a': {'b': {'c': {'d': 'value'}}}}
        self.assertTrue(self.module.has_attr(nested_dict, 'keys'))

    def test_special_attribute_names(self):
        """Test with special attribute names"""

        class TestObj(object):
            pass

        obj = TestObj()
        self.module.set_attr(obj, "__custom__", "value")
        self.assertEqual(obj.__custom__, "value")


def suite():
    """Create test suite"""
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestObjectsModule))
    test_suite.addTest(unittest.makeSuite(TestObjectsModuleEdgeCases))
    return test_suite


if __name__ == '__main__':
    print "Testing objects_module..."
    print "=" * 70
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    sys.exit(0 if result.wasSuccessful() else 1)
