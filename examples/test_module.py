#!/usr/bin/env python2.7

import example_module

print("Testing Python 2.7 C-API extension module")
print("=========================================")

# Test hello_world function
result1 = example_module.hello_world()
print("hello_world(): %s" % result1)

# Test add_numbers function
result2 = example_module.add_numbers(5, 3)
print("add_numbers(5, 3): %d" % result2)

result3 = example_module.add_numbers(-10, 25)
print("add_numbers(-10, 25): %d" % result3)
