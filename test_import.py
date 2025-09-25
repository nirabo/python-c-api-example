#!/usr/bin/env python2.7

import os
import sys

print("Python version: %s" % sys.version)
print("Current working directory: %s" % os.getcwd())
print("Python path:")
for path in sys.path:
    print("  %s" % path)

print("\nFiles in current directory:")
for f in os.listdir('.'):
    print("  %s" % f)

print("\nTrying to import example_module...")
try:
    import example_module

    print("SUCCESS: Module imported!")
    print("hello_world(): %s" % example_module.hello_world())
    print("add_numbers(5, 3): %d" % example_module.add_numbers(5, 3))
except ImportError as e:
    print("FAILED: %s" % str(e))
