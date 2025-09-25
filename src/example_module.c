#include <Python.h>

static PyObject* hello_world(PyObject* self, PyObject* args) {
  return Py_BuildValue("s", "Hello from C extension!");
}

static PyObject* add_numbers(PyObject* self, PyObject* args) {
  int a, b;
  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }
  return Py_BuildValue("i", a + b);
}

static PyMethodDef ExampleMethods[] = {
    {"hello_world", hello_world, METH_VARARGS, "Return a hello world string"},
    {"add_numbers", add_numbers, METH_VARARGS, "Add two integers"},
    {NULL, NULL, 0, NULL}};

PyMODINIT_FUNC initexample_module(void) {
  Py_InitModule("example_module", ExampleMethods);
}
