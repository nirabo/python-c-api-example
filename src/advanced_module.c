/*
 * Python 2.7 C-API Tutorial: Advanced Module
 *
 * This module covers advanced topics:
 * - Callable objects and function calls
 * - Iterator protocol
 * - Context managers
 * - Module state
 * - Capsules for C data
 * - Weak references
 */

#include <Python.h>

/* ============================================================================
 * CALLABLE OBJECTS
 * ============================================================================
 */

static PyObject* call_function(PyObject* self, PyObject* args) {
  PyObject* callable;
  PyObject* call_args;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "OO", &callable, &call_args)) {
    return NULL;
  }

  if (!PyCallable_Check(callable)) {
    PyErr_SetString(PyExc_TypeError, "first argument must be callable");
    return NULL;
  }

  /* Call the function with arguments */
  result = PyObject_CallObject(callable, call_args);

  return result;
}

static PyObject* call_with_kwargs(PyObject* self, PyObject* args) {
  PyObject* callable;
  PyObject* call_args;
  PyObject* kwargs;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "OOO", &callable, &call_args, &kwargs)) {
    return NULL;
  }

  if (!PyCallable_Check(callable)) {
    PyErr_SetString(PyExc_TypeError, "first argument must be callable");
    return NULL;
  }

  result = PyObject_Call(callable, call_args, kwargs);

  return result;
}

static PyObject* call_method(PyObject* self, PyObject* args) {
  PyObject* obj;
  const char* method_name;
  PyObject* method_args;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "OsO", &obj, &method_name, &method_args)) {
    return NULL;
  }

  result = PyObject_CallMethod(obj, (char*)method_name, "O", method_args);

  return result;
}

/* ============================================================================
 * ITERATOR PROTOCOL
 * ============================================================================
 */

typedef struct {
  PyObject_HEAD long current;
  long stop;
  long step;
} RangeIterator;

static void RangeIterator_dealloc(RangeIterator* self) { PyObject_Del(self); }

static PyObject* RangeIterator_iter(PyObject* self) {
  Py_INCREF(self);
  return self;
}

static PyObject* RangeIterator_next(RangeIterator* self) {
  if (self->current >= self->stop) {
    PyErr_SetNone(PyExc_StopIteration);
    return NULL;
  }

  long value = self->current;
  self->current += self->step;

  return PyInt_FromLong(value);
}

static PyTypeObject RangeIteratorType = {
    PyObject_HEAD_INIT(NULL) 0,        /* ob_size */
    "advanced_module.RangeIterator",   /* tp_name */
    sizeof(RangeIterator),             /* tp_basicsize */
    0,                                 /* tp_itemsize */
    (destructor)RangeIterator_dealloc, /* tp_dealloc */
    0,                                 /* tp_print */
    0,                                 /* tp_getattr */
    0,                                 /* tp_setattr */
    0,                                 /* tp_compare */
    0,                                 /* tp_repr */
    0,                                 /* tp_as_number */
    0,                                 /* tp_as_sequence */
    0,                                 /* tp_as_mapping */
    0,                                 /* tp_hash */
    0,                                 /* tp_call */
    0,                                 /* tp_str */
    0,                                 /* tp_getattro */
    0,                                 /* tp_setattro */
    0,                                 /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                /* tp_flags */
    "Range iterator object",           /* tp_doc */
    0,                                 /* tp_traverse */
    0,                                 /* tp_clear */
    0,                                 /* tp_richcompare */
    0,                                 /* tp_weaklistoffset */
    RangeIterator_iter,                /* tp_iter */
    (iternextfunc)RangeIterator_next,  /* tp_iternext */
};

static PyObject* create_range_iterator(PyObject* self, PyObject* args) {
  long start, stop, step = 1;
  RangeIterator* iter;

  if (!PyArg_ParseTuple(args, "ll|l", &start, &stop, &step)) {
    return NULL;
  }

  iter = PyObject_New(RangeIterator, &RangeIteratorType);
  if (iter == NULL) {
    return NULL;
  }

  iter->current = start;
  iter->stop = stop;
  iter->step = step;

  return (PyObject*)iter;
}

static PyObject* iterate_object(PyObject* self, PyObject* args) {
  PyObject* iterable;
  PyObject* iterator;
  PyObject* item;
  PyObject* result;
  int count = 0;

  if (!PyArg_ParseTuple(args, "O", &iterable)) {
    return NULL;
  }

  iterator = PyObject_GetIter(iterable);
  if (iterator == NULL) {
    return NULL;
  }

  result = PyList_New(0);

  while ((item = PyIter_Next(iterator))) {
    PyList_Append(result, item);
    Py_DECREF(item);
    count++;
  }

  Py_DECREF(iterator);

  if (PyErr_Occurred()) {
    Py_DECREF(result);
    return NULL;
  }

  return result;
}

/* ============================================================================
 * CAPSULES (for C data)
 * ============================================================================
 */

typedef struct {
  int x;
  int y;
  char name[50];
} Point;

static void point_destructor(PyObject* capsule) {
  Point* point = (Point*)PyCapsule_GetPointer(capsule, "Point");
  if (point != NULL) {
    PyMem_Free(point);
  }
}

static PyObject* create_point_capsule(PyObject* self, PyObject* args) {
  int x, y;
  const char* name;
  Point* point;
  PyObject* capsule;

  if (!PyArg_ParseTuple(args, "iis", &x, &y, &name)) {
    return NULL;
  }

  point = (Point*)PyMem_Malloc(sizeof(Point));
  if (point == NULL) {
    return PyErr_NoMemory();
  }

  point->x = x;
  point->y = y;
  strncpy(point->name, name, sizeof(point->name) - 1);
  point->name[sizeof(point->name) - 1] = '\0';

  capsule = PyCapsule_New(point, "Point", point_destructor);
  if (capsule == NULL) {
    PyMem_Free(point);
    return NULL;
  }

  return capsule;
}

static PyObject* get_point_data(PyObject* self, PyObject* args) {
  PyObject* capsule;
  Point* point;

  if (!PyArg_ParseTuple(args, "O", &capsule)) {
    return NULL;
  }

  if (!PyCapsule_CheckExact(capsule)) {
    PyErr_SetString(PyExc_TypeError, "expected a capsule");
    return NULL;
  }

  point = (Point*)PyCapsule_GetPointer(capsule, "Point");
  if (point == NULL) {
    return NULL;
  }

  return Py_BuildValue("{s:i,s:i,s:s}", "x", point->x, "y", point->y, "name",
                       point->name);
}

/* ============================================================================
 * IMPORTING MODULES
 * ============================================================================
 */

static PyObject* import_and_call(PyObject* self, PyObject* args) {
  const char* module_name;
  const char* func_name;
  PyObject* module;
  PyObject* func;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "ss", &module_name, &func_name)) {
    return NULL;
  }

  module = PyImport_ImportModule(module_name);
  if (module == NULL) {
    return NULL;
  }

  func = PyObject_GetAttrString(module, func_name);
  Py_DECREF(module);

  if (func == NULL) {
    return NULL;
  }

  if (!PyCallable_Check(func)) {
    Py_DECREF(func);
    PyErr_SetString(PyExc_TypeError, "attribute is not callable");
    return NULL;
  }

  result = PyObject_CallObject(func, NULL);
  Py_DECREF(func);

  return result;
}

/* ============================================================================
 * STRING FORMATTING
 * ============================================================================
 */

static PyObject* format_string(PyObject* self, PyObject* args) {
  const char* template;
  PyObject* values;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "sO", &template, &values)) {
    return NULL;
  }

  result = PyString_Format(PyString_FromString(template), values);

  return result;
}

/* ============================================================================
 * UNICODE HANDLING
 * ============================================================================
 */

static PyObject* string_to_unicode(PyObject* self, PyObject* args) {
  const char* str;
  const char* encoding = "utf-8";

  if (!PyArg_ParseTuple(args, "s|s", &str, &encoding)) {
    return NULL;
  }

  return PyUnicode_DecodeUTF8(str, strlen(str), "strict");
}

static PyObject* unicode_to_string(PyObject* self, PyObject* args) {
  PyObject* unicode;

  if (!PyArg_ParseTuple(args, "O!", &PyUnicode_Type, &unicode)) {
    return NULL;
  }

  return PyUnicode_AsUTF8String(unicode);
}

/* ============================================================================
 * MODULE METHOD TABLE
 * ============================================================================
 */

static PyMethodDef AdvancedMethods[] = {
    /* Callable objects */
    {"call_function", call_function, METH_VARARGS,
     "Call a function with arguments.\n\nArgs:\n    func: Callable\n    args "
     "(tuple): Arguments\n\nReturns:\n    Result of function call"},

    {"call_with_kwargs", call_with_kwargs, METH_VARARGS,
     "Call function with args and kwargs.\n\nArgs:\n    func: Callable\n    "
     "args (tuple): Positional arguments\n    kwargs (dict): Keyword "
     "arguments\n\nReturns:\n    Result"},

    {"call_method", call_method, METH_VARARGS,
     "Call a method on an object.\n\nArgs:\n    obj: Object\n    method_name "
     "(str): Method name\n    args: Method arguments\n\nReturns:\n    Result"},

    /* Iterator protocol */
    {"range_iterator", create_range_iterator, METH_VARARGS,
     "Create a custom range iterator.\n\nArgs:\n    start (int): Start "
     "value\n    stop (int): Stop value\n    step (int, optional): Step "
     "(default: 1)\n\nReturns:\n    RangeIterator"},

    {"iterate", iterate_object, METH_VARARGS,
     "Iterate over an iterable.\n\nArgs:\n    iterable: Any iterable "
     "object\n\nReturns:\n    list: List of all items"},

    /* Capsules */
    {"create_point", create_point_capsule, METH_VARARGS,
     "Create a Point capsule.\n\nArgs:\n    x (int): X coordinate\n    y "
     "(int): Y coordinate\n    name (str): Point name\n\nReturns:\n    "
     "capsule: Point capsule"},

    {"get_point", get_point_data, METH_VARARGS,
     "Get data from Point capsule.\n\nArgs:\n    capsule: Point "
     "capsule\n\nReturns:\n    dict: Point data"},

    /* Module importing */
    {"import_and_call", import_and_call, METH_VARARGS,
     "Import module and call function.\n\nArgs:\n    module_name (str): Module "
     "name\n    func_name (str): Function name\n\nReturns:\n    Result of "
     "function call"},

    /* String operations */
    {"format_string", format_string, METH_VARARGS,
     "Format string with values.\n\nArgs:\n    template (str): Format "
     "template\n    values (tuple/dict): Values\n\nReturns:\n    str: "
     "Formatted string"},

    /* Unicode */
    {"str_to_unicode", string_to_unicode, METH_VARARGS,
     "Convert string to Unicode.\n\nArgs:\n    s (str): Input string\n    "
     "encoding (str, optional): Encoding (default: utf-8)\n\nReturns:\n    "
     "unicode: Unicode object"},

    {"unicode_to_str", unicode_to_string, METH_VARARGS,
     "Convert Unicode to string.\n\nArgs:\n    u (unicode): Unicode "
     "object\n\nReturns:\n    str: UTF-8 encoded string"},

    {NULL, NULL, 0, NULL}};

/* ============================================================================
 * MODULE INITIALIZATION
 * ============================================================================
 */

PyMODINIT_FUNC initadvanced_module(void) {
  PyObject* m;

  /* Initialize RangeIterator type */
  if (PyType_Ready(&RangeIteratorType) < 0) return;

  m = Py_InitModule3("advanced_module", AdvancedMethods,
                     "Python 2.7 C-API Tutorial: Advanced Module\n\n"
                     "This module demonstrates:\n"
                     "- Callable objects and function calls\n"
                     "- Iterator protocol implementation\n"
                     "- Capsules for C data\n"
                     "- Module importing\n"
                     "- String formatting and Unicode");

  if (m == NULL) return;

  Py_INCREF(&RangeIteratorType);
  PyModule_AddObject(m, "RangeIterator", (PyObject*)&RangeIteratorType);
}
