# Python 2.7 C-API Tutorial Suite

A comprehensive, production-ready tutorial for learning the Python 2.7 C-API
through hands-on examples. This project features **6 complete C extension
modules** covering all major C-API topics, **174 comprehensive tests** with
100% pass rate, Docker containerization, and Jupyter notebook integration.

## 🎯 What You'll Learn

This tutorial suite provides complete coverage of the Python 2.7 C-API:

- **Fundamentals**: Argument parsing, return values, type conversions
- **Object Manipulation**: Lists, dicts, tuples, sets, attributes
- **Memory Management**: Reference counting, PyMem_Malloc/Free, safety patterns
- **Exception Handling**: Standard and custom exceptions, error propagation
- **Advanced Topics**: Iterators, capsules, callables, Unicode handling
- **Best Practices**: Memory safety, proper cleanup, error handling patterns

## 📁 Project Structure

```text
pycapi/
├── src/                           # C extension modules (6 modules)
│   ├── example_module.c           # Original simple example
│   ├── basics_module.c            # Fundamental C-API concepts
│   ├── objects_module.c           # Object manipulation
│   ├── memory_module.c            # Memory management patterns
│   ├── exceptions_module.c        # Exception handling
│   ├── advanced_module.c          # Advanced C-API features
│   └── README.md                  # Module documentation
├── tests/                         # Comprehensive test suite (174 tests)
│   ├── test_basics_module.py      # 60+ tests for basics
│   ├── test_objects_module.py     # 50+ tests for objects
│   ├── test_memory_module.py      # 40+ tests with stress testing
│   ├── test_exceptions_module.py  # 50+ tests for exceptions
│   ├── test_advanced_module.py    # 50+ tests for advanced features
│   ├── run_all_tests.py           # Unified test runner
│   └── README.md                  # Testing documentation
├── notebooks/
│   └── complete_capi_tutorial.ipynb  # Comprehensive Jupyter tutorial
├── examples/
│   └── test_module.py             # Python test script
├── scripts/                       # Utility scripts
│   ├── build.sh                   # Build automation script
│   └── test_import.py             # Import diagnostic tool
├── setup.py                       # Extension build configuration
├── Dockerfile                     # Docker environment setup
├── docker-compose.yml             # Docker services configuration
├── Makefile                       # Build automation (primary interface)
├── CLAUDE.md                      # Developer guidance for Claude Code
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Make (optional, but recommended)

### Get Started in 3 Steps

```bash
# 1. Clone and enter directory
git clone <repository-url>
cd pycapi

# 2. Build and run tests
make test

# 3. Start Jupyter notebook for interactive learning
make jupyter
# Access at http://localhost:8888 (check terminal for token)
```

## 📚 Tutorial Modules

### Module 1: basics_module ([src/basics_module.c](src/basics_module.c))

**Fundamental C-API concepts** - Start here!

- Argument parsing: `PyArg_ParseTuple`, `PyArg_ParseTupleAndKeywords`
- Return value building: `Py_BuildValue`
- Type conversions: strings, integers, floats, booleans
- Optional and keyword arguments
- Multiple return values (tuples and dictionaries)
- None handling

**Example functions**: `hello_world`, `add_numbers`, `greet_name`,
`divide_safe`, `power`, `get_statistics`

### Module 2: objects_module ([src/objects_module.c](src/objects_module.c))

Working with Python objects from C:

- List creation and manipulation: `PyList_New`, `PyList_Append`, `PyList_Reverse`
- Dictionary operations: `PyDict_New`, `PyDict_SetItem`, `PyDict_GetItem`
- Tuple creation: `PyTuple_New`, `PyTuple_SetItem`
- Set operations: `PySet_New`, `PySet_Add`, union/intersection
- Attribute manipulation: `PyObject_GetAttr`, `PyObject_SetAttr`
- Type checking and comparison

**Example functions**: `create_list`, `merge_dicts`, `create_tuple`,
`set_union`, `get_attr`, `check_type`

### Module 3: memory_module ([src/memory_module.c](src/memory_module.c))

Critical memory management patterns:

- Reference counting: `Py_INCREF`, `Py_DECREF`, `Py_XDECREF`
- Memory allocation: `PyMem_Malloc`, `PyMem_Free`
- Borrowed vs owned references
- Proper cleanup patterns
- Exception-safe code
- Memory leak prevention

**Example functions**: `allocate_buffer`, `copy_string`, `get_refcount`,
`borrowed_ref_demo`, `proper_cleanup`

### Module 4: exceptions_module ([src/exceptions_module.c](src/exceptions_module.c))

Exception handling and error propagation:

- Raising exceptions: `PyErr_SetString`, `PyErr_Format`
- Standard exceptions: TypeError, ValueError, RuntimeError
- Custom exception types: `PyErr_NewException`
- Exception checking and clearing
- Error propagation patterns
- Validation and error recovery

**Example functions**: `raise_error`, `validate_positive`, `safe_divide`,
custom exceptions (`CustomError`, `ValidationError`)

### Module 5: advanced_module ([src/advanced_module.c](src/advanced_module.c))

Advanced C-API features:

- Iterator protocol implementation: `tp_iter`, `tp_iternext`
- Capsules for C data structures: `PyCapsule_New`, `PyCapsule_GetPointer`
- Callable objects and function calls: `PyObject_Call`, `PyObject_CallMethod`
- Unicode handling: string/unicode conversions
- Module importing from C
- Custom type creation (`RangeIterator`)

**Example functions**: `range_iterator`, `iterate`, `create_point`,
`call_function`, `str_to_unicode`

### Module 6: example_module ([src/example_module.c](src/example_module.c))

**Original simple example** - Good for absolute beginners

- Basic "Hello World" C extension
- Simple integer addition
- Minimal example to understand module structure

## 🧪 Testing

### Run All Tests (174 tests, 100% pass rate)

```bash
make test                 # Run all 174 tests
```

### Run Individual Module Tests

```bash
make test-basics          # Test basics_module (60+ tests)
make test-objects         # Test objects_module (50+ tests)
make test-memory          # Test memory_module (40+ tests)
make test-exceptions      # Test exceptions_module (50+ tests)
make test-advanced        # Test advanced_module (50+ tests)
make test-example         # Test original example_module
```

### Test Coverage

The test suite includes:

- **Normal functionality testing** - Verifies all functions work correctly
- **Edge cases** - Boundary conditions, empty inputs, special values
- **Error handling** - Invalid arguments, type errors, exceptions
- **Memory safety** - Stress tests, leak detection, reference counting
- **Performance** - Large inputs, iteration limits

See [tests/README.md](tests/README.md) for detailed testing documentation.

## 🔧 Development Workflow

### Using Make (Recommended)

```bash
# Show all available commands
make help

# Primary development commands
make dev              # Build C extension and run tests in Docker
make jupyter          # Start Jupyter notebook server (port 8888)
make shell            # Interactive development shell in container

# Testing
make test             # Run all test suites
make test-basics      # Run specific module tests
make debug            # Run diagnostic script to debug issues
make profile          # Performance profiling of C extension

# Container management
make build            # Build Docker images
make down             # Stop all containers
make clean            # Clean build artifacts and Docker resources
make rebuild          # Full rebuild (clean + build)

# Code quality
make pre-commit       # Run pre-commit hooks (linting, formatting, tests)
```

### Interactive Development

```bash
# Enter interactive shell
make shell

# Inside container, build and test:
python setup.py build_ext --inplace
python tests/run_all_tests.py
python -c "import basics_module; print(basics_module.hello_world())"
```

### Jupyter Notebook Workflow

```bash
# Start Jupyter server
make jupyter

# Access at http://localhost:8888 (check logs for token)
# Open: notebooks/complete_capi_tutorial.ipynb
```

**Important**: After modifying C code:

1. Rebuild: `python setup.py build_ext --inplace` (in container)
2. Restart Jupyter kernel: Kernel → Restart
3. Python-only changes don't require rebuild

## 🐳 Docker Environment

The Docker setup provides a complete, reproducible development environment:

- **Ubuntu 18.04** base image
- **Python 2.7** with development headers
- **Build tools**: gcc, make, build-essential
- **Jupyter notebook** server
- **All C extensions** pre-built

### Docker Services

- **jupyter**: Jupyter notebook server on port 8888
- **pycapi-dev**: Interactive development container
- **pycapi-build**: Build and test automation

### Docker Architecture

Multi-stage builds for optimization:

1. **Builder stage**: Compiles C extensions with all build dependencies
2. **Runtime stage**: Minimal runtime + development tools, copies compiled `.so`
   files

This reduces image size while maintaining full development capabilities.

## 📖 Learning Path

### For Beginners

1. Start with **example_module** - understand basic structure
2. Move to **basics_module** - learn fundamental concepts
3. Study **objects_module** - work with Python objects
4. Master **memory_module** - critical for writing safe C code
5. Learn **exceptions_module** - proper error handling
6. Explore **advanced_module** - powerful features

### For Experienced Developers

- Jump directly to relevant modules
- Each module is self-contained with complete documentation
- Use tests as examples for each function
- Refer to [src/README.md](src/README.md) for detailed API docs

### Using the Jupyter Notebook

The comprehensive tutorial notebook
([notebooks/complete_capi_tutorial.ipynb](notebooks/complete_capi_tutorial.ipynb))
provides:

- Interactive examples for all modules
- Explanations of key concepts
- Hands-on exercises
- Performance comparisons
- Visual demonstrations

## 📊 Performance

C extensions provide significant performance benefits for computational tasks:

```python
import example_module
import time

# Benchmark C extension
start = time.time()
for i in range(1000000):
    result = example_module.add_numbers(i, i+1)
c_time = time.time() - start

# Compare with Python
def python_add(a, b):
    return a + b

start = time.time()
for i in range(1000000):
    result = python_add(i, i+1)
python_time = time.time() - start

print("C extension: %.4f seconds" % c_time)
print("Python: %.4f seconds" % python_time)
print("Speedup: %.2fx" % (python_time / c_time))
```

Run performance profiling:

```bash
make profile
```

## 🔍 Troubleshooting

### Import Errors

```bash
# 1. Ensure modules are built
make dev

# 2. Run diagnostic script
make debug

# 3. Check if .so files exist
make shell
ls -la *.so
```

### Build Failures

```bash
# Check Docker installation
docker --version
docker compose version

# Clean rebuild
make rebuild

# Check build logs
make logs
```

### Test Failures

```bash
# Run specific failing module
make test-basics  # or test-objects, test-memory, etc.

# Run single test file
docker compose run --rm pycapi-dev python tests/test_basics_module.py

# Interactive debugging
make shell
python -c "import basics_module; basics_module.add_numbers(1, 2)"
```

### Jupyter Issues

- **Can't find module**: Restart kernel after rebuilding C extension
- **Connection refused**: Check if container is running: `docker compose ps`
- **Token required**: Check logs: `make logs`

## 🎓 Key C-API Concepts Covered

### Reference Counting (Critical!)

```c
// Increment reference count (ownership)
Py_INCREF(obj);

// Decrement reference count (release)
Py_DECREF(obj);

// Safe decrement (NULL check)
Py_XDECREF(obj);
```

### Argument Parsing

```c
// Parse tuple arguments
const char* name;
int age;
PyArg_ParseTuple(args, "si", &name, &age);

// Parse keyword arguments
static char *kwlist[] = {"name", "age", NULL};
PyArg_ParseTupleAndKeywords(args, kwargs, "si", kwlist, &name, &age);
```

### Return Values

```c
// Build simple values
return Py_BuildValue("i", 42);              // int
return Py_BuildValue("s", "hello");         // string
return Py_BuildValue("(ii)", 10, 20);       // tuple

// Return None
Py_RETURN_NONE;
```

### Exception Handling

```c
// Set exception and return NULL
PyErr_SetString(PyExc_ValueError, "Invalid input");
return NULL;

// Format exception message
PyErr_Format(PyExc_TypeError, "Expected int, got %s", type_name);
return NULL;
```

### Memory Management

```c
// Allocate memory
char* buffer = (char*)PyMem_Malloc(size);
if (buffer == NULL) {
    return PyErr_NoMemory();
}

// Use buffer...

// Always free
PyMem_Free(buffer);
```

## 📚 Additional Resources

### Official Python 2.7 C-API Documentation

- [Python 2.7 C-API Reference](https://docs.python.org/2.7/c-api/)
- [Extending and Embedding Python](https://docs.python.org/2.7/extending/)
- [Python/C API Reference Manual](https://docs.python.org/2.7/c-api/index.html)

### Modern Alternatives

- [Cython](https://cython.org/) - Python-like syntax compiled to C
- [pybind11](https://github.com/pybind/pybind11) - Modern C++11 bindings
- [CFFI](https://cffi.readthedocs.io/) - Foreign Function Interface
- [ctypes](https://docs.python.org/3/library/ctypes.html) - Call C from Python

### Python 3 Migration

For Python 3.x C-API (recommended for production):

- [Python 3 C-API Docs](https://docs.python.org/3/c-api/)
- [Porting Extension Modules to
  Python 3](https://docs.python.org/3/howto/cporting.html)

## ⚠️ Python 2.7 Notice

**This project uses Python 2.7 for educational purposes only.**

Python 2.7 reached end-of-life on January 1, 2020. The C-API concepts taught
here are transferable to Python 3, but syntax and some APIs have changed.

**For production use**: Migrate to Python 3.x and use the Python 3 C-API.

## 🤝 Contributing

Contributions are welcome! This is an educational project.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and test thoroughly (`make test`)
4. Ensure code quality (`make pre-commit`)
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Follow existing code style (Google C style, black for Python)
- Add tests for new functionality (maintain 100% pass rate)
- Update documentation (README, CLAUDE.md, module docs)
- Test in Docker environment (`make test`)
- Run pre-commit hooks (`make pre-commit`)

## 🏆 Project Status

- ✅ **6 complete C extension modules** covering all major C-API topics
- ✅ **174 comprehensive tests** with **100% pass rate**
- ✅ Full Docker development environment
- ✅ Jupyter notebook integration
- ✅ Complete documentation (README, CLAUDE.md, module docs, test docs)
- ✅ CI/CD pipeline with GitHub Actions
- ✅ Pre-commit hooks for code quality

## 📄 License

This project is for educational purposes. Feel free to use, modify, and learn
from it.

## 🙏 Acknowledgments

- Python Software Foundation for the excellent C-API documentation
- The Python community for tutorials and examples
- Contributors and users of this educational project

---

## 📞 Support & Feedback

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Check [CLAUDE.md](CLAUDE.md) for developer guidance

---

**Happy learning! 🚀 Master the Python C-API and unlock high-performance Python
extensions.**
