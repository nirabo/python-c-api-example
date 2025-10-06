# C Extension Modules

This directory contains comprehensive Python 2.7 C-API tutorial modules organized by topic.

## Module Overview

### example_module.c

**Simple introductory module** demonstrating basic C extension concepts.

**Functions:**

- `hello_world()` - Returns a greeting string
- `add_numbers(a, b)` - Integer addition

**Topics:** Basic module structure, simple function definitions

---

### basics_module.c

**Fundamental C-API concepts** - Start here for the tutorial.

**Topics:**

- Argument parsing (`PyArg_ParseTuple`, `PyArg_ParseTupleAndKeywords`)
- Return value building (`Py_BuildValue`)
- Type handling (strings, integers, floats, booleans)
- Optional and keyword arguments
- Multiple return values (tuples and dicts)
- None handling (`Py_RETURN_NONE`)

**Key Functions:**

- `hello_world()`, `greet_name(name)`
- `add_numbers(a, b)`, `multiply_floats(a, b)`, `divide_safe(a, b)`
- `is_even(num)`, `string_length(s)`
- `power(base, exponent=2.0)` - keyword arguments
- `divmod(a, b)` - returns tuple
- `get_statistics(value)` - returns dictionary

---

### objects_module.c

**Object manipulation and Python object protocols**

**Topics:**

- List operations (`PyList_New`, `PyList_Size`, `PyList_GetItem`, `PyList_SET_ITEM`)
- Dictionary operations (`PyDict_New`, `PyDict_SetItem`, `PyDict_GetItemString`)
- Tuple operations (`PyTuple_New`, `PyTuple_GetItem`)
- Set operations (`PySet_New`, `PyNumber_Or`)
- Attribute access (`PyObject_GetAttrString`, `PyObject_SetAttrString`, `PyObject_HasAttrString`)
- Type checking (`PyInt_Check`, `PyList_Check`, `PyDict_Check`, etc.)
- Object comparison (`PyObject_Compare`)

**Key Functions:**

- `create_list(size)`, `sum_list(lst)`, `reverse_list(lst)`
- `create_dict()`, `dict_has_key(d, key)`, `merge_dicts(d1, d2)`
- `create_tuple(size)`, `tuple_element(t, index)`
- `get_attr(obj, name)`, `set_attr(obj, name, value)`, `has_attr(obj, name)`
- `get_type(obj)`, `check_type(obj)`, `compare(obj1, obj2)`

---

### memory_module.c

**Memory management and reference counting** - Critical concepts!

**Topics:**

- Reference counting (`Py_INCREF`, `Py_DECREF`, `Py_XDECREF`)
- Memory allocation (`PyMem_Malloc`, `PyMem_Free`)
- Borrowed vs owned references
- Memory leak prevention
- Exception-safe cleanup (goto error pattern)
- Object lifecycle management

**Key Functions:**

- `get_refcount(obj)` - Get reference count
- `incref_demo(obj)` - Demonstrate INCREF/DECREF
- `create_temp_list(size)` - Temporary object creation/cleanup
- `allocate_buffer(size)` - PyMem_Malloc/Free demonstration
- `borrowed_ref_demo(lst)` - Borrowed reference handling
- `owned_ref_demo(value)` - Owned reference handling
- `proper_cleanup(str1, str2)` - Safe memory management
- `exception_safe()` - Exception-safe coding pattern

**Important Patterns:**

```c
/* Borrowed reference - don't DECREF */
item = PyList_GetItem(list, 0);  // BORROWED

/* Owned reference - must DECREF */
item = PyInt_FromLong(42);  // NEW reference
Py_DECREF(item);

/* Exception-safe cleanup */
PyObject* result = NULL;
// ... code ...
error:
    Py_XDECREF(result);
    return NULL;
```

---

### exceptions_module.c

**Exception handling and error propagation**

**Topics:**

- Raising standard exceptions (`PyErr_SetString`, `PyErr_Format`)
- Custom exception types (`PyErr_NewException`)
- Exception checking (`PyErr_Occurred`, `PyErr_ExceptionMatches`)
- Exception clearing (`PyErr_Clear`)
- Exception info retrieval (`PyErr_Fetch`)
- Exception propagation through nested calls
- Warning generation (`PyErr_WarnEx`)

**Custom Exceptions:**

- `CustomError` - General custom exception
- `ValidationError` - Validation-specific exception

**Key Functions:**

- `raise_value_error(msg)`, `raise_type_error()`, `raise_runtime_error()`
- `raise_custom_error(msg)`, `raise_validation_error(field, reason)`
- `check_and_clear(callable)` - Call and clear exceptions
- `check_exception_type(callable)` - Identify exception type
- `get_exception_info(callable)` - Extract exception details
- `safe_divide(a, b)` - Exception propagation example

**Error Handling Pattern:**

```c
if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;  // Propagate parsing error
}

if (b == 0) {
    PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
    return NULL;
}
```

---

### advanced_module.c

**Advanced C-API topics**

**Topics:**

- Callable objects (`PyCallable_Check`, `PyObject_CallObject`, `PyObject_Call`)
- Method calls (`PyObject_CallMethod`)
- Iterator protocol implementation (custom RangeIterator type)
- Capsules for C data structures (`PyCapsule_New`, `PyCapsule_GetPointer`)
- Module importing (`PyImport_ImportModule`)
- String formatting (`PyString_Format`)
- Unicode handling (`PyUnicode_DecodeUTF8`, `PyUnicode_AsUTF8String`)

**Custom Types:**

- `RangeIterator` - Complete iterator protocol implementation

**Key Functions:**

- `call_function(func, args)` - Call callable with args tuple
- `call_with_kwargs(func, args, kwargs)` - Call with keyword arguments
- `call_method(obj, method_name, args)` - Invoke object method
- `range_iterator(start, stop, step)` - Create custom iterator
- `iterate(iterable)` - Iterate over any iterable
- `create_point(x, y, name)` - Create Point capsule
- `get_point(capsule)` - Extract data from capsule
- `import_and_call(module_name, func_name)` - Import and execute
- `format_string(template, values)` - String formatting
- `str_to_unicode(s)`, `unicode_to_str(u)` - Unicode conversion

---

## Build Instructions

All modules are built together using setup.py:

```bash
python setup.py build_ext --inplace
```

This generates `.so` files in the project root:

- `example_module.so`
- `basics_module.so`
- `objects_module.so`
- `memory_module.so`
- `exceptions_module.so`
- `advanced_module.so`

## Testing

Import and test each module:

```python
import basics_module
print basics_module.hello_world()
print basics_module.add_numbers(5, 3)
```

Or use the comprehensive Jupyter notebook: `notebooks/complete_capi_tutorial.ipynb`

## Learning Path

1. **basics_module** - Start here for fundamentals
2. **objects_module** - Learn object manipulation
3. **memory_module** - Master reference counting (CRITICAL!)
4. **exceptions_module** - Handle errors properly
5. **advanced_module** - Explore advanced features

## Key Concepts

### Reference Counting Rules

1. **Functions that return NEW references** (you must DECREF):
   - `PyInt_FromLong`, `PyFloat_FromDouble`, `PyString_FromString`
   - `PyList_New`, `PyDict_New`, `PyTuple_New`
   - `Py_BuildValue`

2. **Functions that return BORROWED references** (don't DECREF):
   - `PyList_GetItem`, `PyTuple_GetItem`
   - `PyDict_GetItem`, `PyDict_GetItemString`
   - `PyObject_GetAttrString` returns NEW reference!

3. **Functions that STEAL references**:
   - `PyList_SET_ITEM`, `PyTuple_SET_ITEM`

### Error Handling

Always return `NULL` on error and set exception:

```c
if (error_condition) {
    PyErr_SetString(PyExc_ValueError, "error message");
    return NULL;
}
```

### Memory Safety

```c
char* buffer = PyMem_Malloc(size);
if (buffer == NULL) {
    return PyErr_NoMemory();
}

// ... use buffer ...

PyMem_Free(buffer);  // Always free!
```

## Documentation

- Python 2.7 C-API: <https://docs.python.org/2.7/c-api/>
- Extending Python: <https://docs.python.org/2.7/extending/>
- Complete tutorial: `notebooks/complete_capi_tutorial.ipynb`
