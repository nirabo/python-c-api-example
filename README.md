# Python 2.7 C-API Extension Project

A complete development environment for creating Python 2.7 C extensions using
the Python C-API, featuring Docker containerization and Jupyter notebook
integration.

## 🎯 Project Overview

This project demonstrates how to:

- Create Python C extensions using the Python 2.7 C-API
- Set up a complete Docker-based development environment
- Use Jupyter notebooks for interactive development and testing
- Build, test, and debug C extensions efficiently

## 📁 Project Structure

```text
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

# Build and test in Docker container
make dev

# Interactive development shell
make shell
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

### Option 3: Direct Commands

```bash
# Build and test in container
docker compose up pycapi-build

# Interactive shell
docker compose run --rm pycapi-dev
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

### 2. Container Development

```bash
# Quick development cycle (build and test)
make dev

# Interactive development shell
make shell

# Debug import issues
make debug

# Performance profiling
make profile
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

### Core Commands

- `make dev` - Build and test in Docker container
- `make jupyter` - Start Jupyter notebook server
- `make shell` - Interactive development shell
- `make test` - Run tests in container
- `make debug` - Run diagnostic script
- `make profile` - Performance profiling

### Container Management

- `make build` - Build Docker images
- `make up` - Start services in background
- `make down` - Stop containers
- `make logs` - Show container logs

### Maintenance

- `make clean` - Clean build artifacts and Docker resources
- `make rebuild` - Full rebuild of Docker images
- `make pre-commit` - Run pre-commit hooks

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
make test    # Run tests in container
make dev     # Build and test in one command
```

### Interactive Testing

Use the Jupyter notebook `notebooks/test_capi_extension.ipynb` for:

- Function testing
- Error handling validation
- Performance benchmarking
- Module introspection

### Debugging

```bash
make debug    # Run diagnostic script in container
make shell    # Interactive shell for manual debugging
```

## 🔍 Troubleshooting

### Import Errors

1. Ensure the module is built: `make dev`
2. Check Python path: `make debug`
3. Restart Jupyter kernel if using notebooks

### Docker Issues

```bash
make clean     # Clean Docker resources
make rebuild   # Full rebuild
make logs      # Check container logs
```

### Build Failures

1. Check Docker installation
2. Verify container can build: `make build`
3. Check logs: `make logs`

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

This project uses Python 2.7 for educational purposes. Python 2.7 reached
end-of-life on January 1, 2020. For production use, consider migrating to
Python 3.x.

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
- [pybind11](https://github.com/pybind/pybind11) - Modern C++ bindings

---

## Happy coding! 🚀
