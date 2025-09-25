# Python 2.7 C-API Extension Project

A complete development environment for creating Python 2.7 C extensions using the Python C-API, featuring Docker containerization and Jupyter notebook integration.

## 🎯 Project Overview

This project demonstrates how to:

- Create Python C extensions using the Python 2.7 C-API
- Set up a complete Docker-based development environment
- Use Jupyter notebooks for interactive development and testing
- Build, test, and debug C extensions efficiently

## 📁 Project Structure

```
pycapi/
├── src/
│   └── example_module.c       # C extension source code
├── notebooks/
│   └── test_capi_extension.ipynb  # Jupyter notebook for testing
├── examples/
│   └── test_module.py         # Python test script
├── tests/                     # Test directory (future tests)
├── setup.py                   # Extension build configuration
├── Dockerfile                 # Docker environment setup
├── docker-compose.yml         # Docker services configuration
├── Makefile                   # Build automation
├── build.sh                   # Build script
└── test_import.py             # Import diagnostic script
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Make (optional, but recommended)

### Option 1: Using Make (Recommended)

```bash
# Show all available commands
make help

# Start Jupyter notebook server
make jupyter

# Build and test locally (requires Python 2.7)
make dev

# Interactive Docker development
make docker-dev
```

### Option 2: Using Docker Compose Directly

```bash
# Start Jupyter notebook server
docker compose up jupyter

# Build and test in container
docker compose up pycapi-build

# Interactive development shell
docker compose run --rm pycapi-dev
```

### Option 3: Local Development

```bash
# Install dependencies (Ubuntu)
sudo apt-get install python2.7 python2.7-dev python-pip build-essential

# Build extension
python2.7 setup.py build_ext --inplace

# Test extension
python2.7 examples/test_module.py
```

## 🔧 Development Workflow

### 1. Jupyter Notebook Development

```bash
make jupyter
```

Access Jupyter at: `http://localhost:8888` (check logs for token)

The notebook environment includes:

- Pre-built C extension module
- Interactive testing capabilities
- Performance benchmarking tools

### 2. Local Development

```bash
# Quick development cycle
make dev  # Builds and tests

# Clean build artifacts
make clean

# Debug import issues
make debug
```

### 3. Container Development

```bash
# Interactive container shell
make docker-dev

# Inside container:
python setup.py build_ext --inplace
python examples/test_module.py
```

## 📝 C Extension API

The `example_module` provides two functions:

### `hello_world()`

Returns a greeting string from the C extension.

```python
import example_module
result = example_module.hello_world()
print(result)  # Output: "Hello from C extension!"
```

### `add_numbers(a, b)`

Adds two integers and returns the result.

```python
import example_module
result = example_module.add_numbers(5, 3)
print(result)  # Output: 8
```

## 🐳 Docker Environment

The Docker setup provides:

- Ubuntu 18.04 base image
- Python 2.7 with development headers
- Build tools (gcc, make, etc.)
- Jupyter notebook server
- Pre-built C extension

### Services

- **jupyter**: Jupyter notebook server on port 8888
- **pycapi-dev**: Interactive development container
- **pycapi-build**: Build and test automation

## 🛠️ Makefile Targets

### Development

- `make build` - Build C extension locally
- `make test` - Run test script
- `make clean` - Clean build artifacts
- `make dev` - Quick build and test cycle

### Docker Operations

- `make jupyter` - Start Jupyter server
- `make docker-dev` - Interactive Docker shell
- `make docker-build-test` - Build and test in container

### Maintenance

- `make docker-clean` - Clean Docker resources
- `make docker-rebuild` - Full Docker rebuild

### Advanced

- `make profile` - Performance profiling
- `make valgrind` - Memory debugging (requires valgrind)
- `make gdb` - Debug with GDB

## 📊 Performance Testing

The project includes performance comparison between C extension and Python:

```python
import example_module
import time

# Benchmark C extension vs Python
start = time.time()
for i in range(100000):
    result = example_module.add_numbers(i, i+1)
c_time = time.time() - start

# Compare with equivalent Python function
def python_add(a, b):
    return a + b

start = time.time()
for i in range(100000):
    result = python_add(i, i+1)
python_time = time.time() - start

print("Speedup: %.2fx" % (python_time / c_time))
```

## 🧪 Testing

### Automated Testing

```bash
make test           # Local testing
make docker-build-test  # Docker testing
```

### Interactive Testing

Use the Jupyter notebook `notebooks/test_capi_extension.ipynb` for:

- Function testing
- Error handling validation
- Performance benchmarking
- Module introspection

### Debugging

```bash
make debug          # Run diagnostic script
make valgrind       # Memory checking
make gdb           # Interactive debugging
```

## 🔍 Troubleshooting

### Import Errors

1. Ensure the module is built: `make build`
2. Check Python path: `make debug`
3. Restart Jupyter kernel if using notebooks

### Docker Issues

```bash
make docker-clean   # Clean Docker resources
make docker-rebuild # Full rebuild
make docker-ps      # Check container status
```

### Build Failures

1. Check Python 2.7 installation
2. Verify development headers are installed
3. Check compiler (gcc) availability

## 📚 Learning Resources

### Python C-API Documentation

- [Python 2.7 C-API Reference](https://docs.python.org/2.7/c-api/)
- [Extending and Embedding Python](https://docs.python.org/2.7/extending/)

### Key C-API Concepts

- **Reference Counting**: Memory management in Python objects
- **PyArg_ParseTuple**: Parsing function arguments
- **Py_BuildValue**: Building return values
- **Module Initialization**: Setting up extension modules

## ⚠️ Python 2.7 Notice

This project uses Python 2.7 for educational purposes. Python 2.7 reached end-of-life on January 1, 2020. For production use, consider migrating to Python 3.x.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test thoroughly
4. Submit a pull request

### Development Guidelines

- Follow existing code style
- Add tests for new functionality
- Update documentation as needed
- Test in both local and Docker environments

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🔗 Related Projects

- [Python C Extension Tutorial](https://docs.python.org/3/extending/extending.html)
- [Cython](https://cython.org/) - Alternative approach to Python extensions
- [pybind11](https://github.com/pybind/pybind11) - Modern C++ bindings for Python

---

**Happy coding! 🚀**
