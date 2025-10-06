from distutils.core import Extension, setup

# Define all C extension modules
example_module = Extension('example_module', sources=['src/example_module.c'])

basics_module = Extension('basics_module', sources=['src/basics_module.c'])

objects_module = Extension('objects_module', sources=['src/objects_module.c'])

memory_module = Extension(
    'memory_module', sources=['src/memory_module.c'], extra_compile_args=['-lm']
)

exceptions_module = Extension('exceptions_module', sources=['src/exceptions_module.c'])

advanced_module = Extension('advanced_module', sources=['src/advanced_module.c'])

setup(
    name='PyCAPI Tutorial Suite',
    version='2.0',
    description='Comprehensive Python 2.7 C-API Tutorial Package',
    author='C-API Tutorial',
    ext_modules=[
        example_module,
        basics_module,
        objects_module,
        memory_module,
        exceptions_module,
        advanced_module,
    ],
)
