#!/bin/bash

# Build and test script for Python 2.7 C-API extension

set -e

echo "Building Python 2.7 C-API extension..."

# Build the extension
python setup.py build_ext --inplace

echo "Extension built successfully!"

# Run tests
echo "Running tests..."
python examples/test_module.py

echo "All tests completed!"

# Clean build artifacts (optional)
echo "Cleaning up build artifacts..."
python setup.py clean --all
rm -rf build/
find . -name "*.so" -delete

echo "Build and test process completed!"
