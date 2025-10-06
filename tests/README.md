# Test Suite for Python 2.7 C-API Tutorial

Comprehensive test coverage for all C extension modules.

## Test Files

### Individual Module Tests

- **[test_basics_module.py](test_basics_module.py)** - Tests for basics_module
  - Argument parsing and type conversions
  - Optional and keyword arguments
  - Multiple return values
  - Edge cases and error handling
  - **60+ test cases**

- **[test_objects_module.py](test_objects_module.py)** - Tests for objects_module
  - List, dict, tuple, and set operations
  - Attribute access and manipulation
  - Type checking and comparison
  - **50+ test cases**

- **[test_memory_module.py](test_memory_module.py)** - Tests for memory_module
  - Reference counting behavior
  - Memory allocation/deallocation
  - Borrowed vs owned references
  - Stress tests for memory leaks
  - **40+ test cases**

- **[test_exceptions_module.py](test_exceptions_module.py)** - Tests for exceptions_module
  - Standard exception raising
  - Custom exception types
  - Exception checking and clearing
  - Exception propagation
  - **50+ test cases**

- **[test_advanced_module.py](test_advanced_module.py)** - Tests for advanced_module
  - Callable objects and function calls
  - Iterator protocol implementation
  - Capsules for C data
  - Module importing and Unicode handling
  - **50+ test cases**

### Test Runner

- **[run_all_tests.py](run_all_tests.py)** - Comprehensive test runner
  - Discovers and runs all test suites
  - Provides detailed summary and coverage report
  - Checks for built modules before running

## Running Tests

### Run All Tests

```bash
# Using Make (recommended)
make test

# Using Docker directly
docker compose run --rm pycapi-dev sh -c "python setup.py build_ext --inplace && python tests/run_all_tests.py"

# Locally (if modules are built)
python tests/run_all_tests.py
```

### Run Individual Module Tests

```bash
# Test specific module
make test-basics      # basics_module tests
make test-objects     # objects_module tests
make test-memory      # memory_module tests
make test-exceptions  # exceptions_module tests
make test-advanced    # advanced_module tests

# Or run directly
python tests/test_basics_module.py
python tests/test_objects_module.py
# etc.
```

### Run in Docker Container

```bash
# Interactive shell with built modules
make shell

# Then inside container:
python tests/run_all_tests.py
python tests/test_basics_module.py
# etc.
```

## Test Coverage

### Total Test Count: **250+ tests**

Coverage by module:

- **basics_module**: 60+ tests covering all functions and edge cases
- **objects_module**: 50+ tests for object manipulation
- **memory_module**: 40+ tests including stress tests
- **exceptions_module**: 50+ tests for all exception scenarios
- **advanced_module**: 50+ tests for advanced features

### What's Tested

#### Basics Module

- ✅ String, integer, float, boolean handling
- ✅ Argument parsing (positional, keyword, optional)
- ✅ Return value building (single, tuple, dict)
- ✅ Type conversions and checking
- ✅ Error handling and edge cases
- ✅ Large values, special characters, Unicode

#### Objects Module

- ✅ List creation, manipulation, iteration
- ✅ Dictionary operations and merging
- ✅ Tuple and set operations
- ✅ Attribute get/set/check
- ✅ Type checking for all basic types
- ✅ Object comparison
- ✅ Empty containers and edge cases

#### Memory Module

- ✅ Reference counting (INCREF/DECREF)
- ✅ Memory allocation (PyMem_Malloc/Free)
- ✅ Borrowed vs owned reference handling
- ✅ Memory leak prevention
- ✅ Exception-safe cleanup
- ✅ Stress tests with large allocations
- ✅ Repeated allocation/deallocation

#### Exceptions Module

- ✅ All standard exceptions (ValueError, TypeError, etc.)
- ✅ Custom exception types (CustomError, ValidationError)
- ✅ Exception checking, clearing, matching
- ✅ Exception info retrieval
- ✅ Exception propagation through nested calls
- ✅ Warning generation
- ✅ Error messages with special characters

#### Advanced Module

- ✅ Calling functions with args/kwargs
- ✅ Method invocation
- ✅ Iterator protocol (custom RangeIterator)
- ✅ Iterating over various containers
- ✅ Capsules for C data structures
- ✅ Module importing and function calling
- ✅ String formatting
- ✅ Unicode conversion (str ↔ unicode)

## Test Output

### Successful Run

```
==============================================================================
Python 2.7 C-API Tutorial - Test Suite
==============================================================================

Checking if C extension modules are built...
  [OK] basics_module
  [OK] objects_module
  [OK] memory_module
  [OK] exceptions_module
  [OK] advanced_module

All modules found. Discovering tests...

------------------------------------------------------------------------------
Running Tests
------------------------------------------------------------------------------

test_hello_world (test_basics_module.TestBasicsModule) ... ok
test_add_numbers (test_basics_module.TestBasicsModule) ... ok
...

==============================================================================
TEST SUMMARY
==============================================================================

Total Tests:    252
Passed:         252
Failed:         0
Errors:         0
Skipped:        0

Success Rate: 100.0%

==============================================================================
ALL TESTS PASSED!
==============================================================================
```

### Failed Run

```
TEST SUMMARY
==============================================================================

Total Tests:    252
Passed:         250
Failed:         2
Errors:         0

FAILURES:
------------------------------------------------------------------------------
  * test_something (test_module.TestClass)
  * test_another (test_module.TestClass)

Success Rate: 99.2%
```

## Test Organization

Each test file follows this structure:

```python
class TestModuleName(unittest.TestCase):
    """Main test cases"""

    @classmethod
    def setUpClass(cls):
        """Import module once"""
        import module_name
        cls.module = module_name

    def test_feature(self):
        """Test specific feature"""
        result = self.module.function()
        self.assertEqual(result, expected)

class TestModuleNameEdgeCases(unittest.TestCase):
    """Edge cases and stress tests"""
    # ...

def suite():
    """Create test suite"""
    return unittest.TestSuite([...])
```

## Adding New Tests

1. Choose appropriate test file or create new one
2. Add test method following naming convention: `test_<description>`
3. Use descriptive docstrings
4. Test normal cases, edge cases, and error conditions
5. Run tests to verify

### Example Test

```python
def test_new_function(self):
    """Test description"""
    # Normal case
    result = self.module.new_function(arg)
    self.assertEqual(result, expected)

    # Edge case
    result = self.module.new_function(edge_case)
    self.assertIsNotNone(result)

    # Error case
    with self.assertRaises(ValueError):
        self.module.new_function(invalid_arg)
```

## Continuous Integration

Tests are automatically run in GitHub Actions CI/CD pipeline:

- Pre-commit checks
- Full test suite on push
- Test matrix for different scenarios

See [.github/workflows/ci.yml](../.github/workflows/ci.yml) for details.

## Best Practices

1. **Test all code paths** - Normal, edge cases, errors
2. **Use descriptive names** - test_function_name_behavior
3. **One assertion per test** - Keep tests focused
4. **Test edge cases** - Empty inputs, large values, special chars
5. **Test error handling** - Use `assertRaises`
6. **Clean up resources** - Use tearDown if needed
7. **Document tests** - Add docstrings explaining what's tested

## Debugging Failed Tests

```bash
# Run single test with verbose output
python tests/test_basics_module.py -v

# Run specific test case
python -m unittest tests.test_basics_module.TestBasicsModule.test_hello_world

# Add print statements
def test_something(self):
    result = self.module.function()
    print "Debug: result =", result  # Add debug output
    self.assertEqual(result, expected)
```

## Test Coverage Goals

- ✅ **100% function coverage** - All functions tested
- ✅ **Branch coverage** - All code paths tested
- ✅ **Error coverage** - All error conditions tested
- ✅ **Edge case coverage** - Boundary conditions tested
- ✅ **Integration coverage** - Module interactions tested

## References

- Python 2.7 unittest: <https://docs.python.org/2.7/library/unittest.html>
- Testing best practices: See CLAUDE.md
