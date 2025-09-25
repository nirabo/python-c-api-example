from distutils.core import Extension, setup

example_module = Extension('example_module', sources=['src/example_module.c'])

setup(
    name='PyCAPI Example',
    version='1.0',
    description='Python 2.7 C-API example package',
    ext_modules=[example_module],
)
