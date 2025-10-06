/*
 * Python 2.7 C-API Tutorial: Basics Module
 *
 * This module covers fundamental concepts:
 * - Basic function definitions
 * - Argument parsing with PyArg_ParseTuple
 * - Building return values with Py_BuildValue
 * - String, integer, float, and boolean handling
 * - Module initialization
 */

#include <Python.h>

/* ============================================================================
 * BASIC FUNCTIONS
 * ============================================================================
 */

static PyObject* hello_world(PyObject* self, PyObject* args) {
  return Py_BuildValue("s", "Hello from C extension!");
}

static PyObject* greet_name(PyObject* self, PyObject* args) {
  const char* name;

  if (!PyArg_ParseTuple(args, "s", &name)) {
    return NULL;
  }

  return PyString_FromFormat("Hello, %s!", name);
}

/* ============================================================================
 * NUMERIC OPERATIONS
 * ============================================================================
 */

static PyObject* add_numbers(PyObject* self, PyObject* args) {
  int a, b;

  if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
    return NULL;
  }

  return Py_BuildValue("i", a + b);
}

static PyObject* multiply_floats(PyObject* self, PyObject* args) {
  double a, b;

  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }

  return Py_BuildValue("d", a * b);
}

static PyObject* divide_safe(PyObject* self, PyObject* args) {
  double a, b;

  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }

  if (b == 0.0) {
    PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
    return NULL;
  }

  return Py_BuildValue("d", a / b);
}

/* ============================================================================
 * TYPE CONVERSIONS AND CHECKING
 * ============================================================================
 */

static PyObject* is_even(PyObject* self, PyObject* args) {
  long num;

  if (!PyArg_ParseTuple(args, "l", &num)) {
    return NULL;
  }

  if (num % 2 == 0) {
    Py_RETURN_TRUE;
  } else {
    Py_RETURN_FALSE;
  }
}

static PyObject* string_length(PyObject* self, PyObject* args) {
  const char* str;
  Py_ssize_t length;

  if (!PyArg_ParseTuple(args, "s#", &str, &length)) {
    return NULL;
  }

  return Py_BuildValue("i", (int)length);
}

/* ============================================================================
 * OPTIONAL ARGUMENTS
 * ============================================================================
 */

static PyObject* power_func(PyObject* self, PyObject* args, PyObject* kwargs) {
  double base, exponent = 2.0;
  static char* kwlist[] = {"base", "exponent", NULL};

  if (!PyArg_ParseTupleAndKeywords(args, kwargs, "d|d", kwlist, &base,
                                   &exponent)) {
    return NULL;
  }

  return Py_BuildValue("d", pow(base, exponent));
}

/* ============================================================================
 * MULTIPLE RETURN VALUES (TUPLES)
 * ============================================================================
 */

static PyObject* divmod_operation(PyObject* self, PyObject* args) {
  long a, b;

  if (!PyArg_ParseTuple(args, "ll", &a, &b)) {
    return NULL;
  }

  if (b == 0) {
    PyErr_SetString(PyExc_ZeroDivisionError, "division by zero");
    return NULL;
  }

  return Py_BuildValue("(ll)", a / b, a % b);
}

static PyObject* get_statistics(PyObject* self, PyObject* args) {
  double value;

  if (!PyArg_ParseTuple(args, "d", &value)) {
    return NULL;
  }

  return Py_BuildValue("{s:d,s:d,s:d}", "value", value, "square", value * value,
                       "cube", value * value * value);
}

/* ============================================================================
 * NONE HANDLING
 * ============================================================================
 */

static PyObject* return_none(PyObject* self, PyObject* args) { Py_RETURN_NONE; }

static PyObject* accept_optional(PyObject* self, PyObject* args) {
  PyObject* obj = NULL;

  if (!PyArg_ParseTuple(args, "|O", &obj)) {
    return NULL;
  }

  if (obj == NULL || obj == Py_None) {
    return Py_BuildValue("s", "No argument provided");
  }

  return PyObject_Str(obj);
}

/* ============================================================================
 * MODULE METHOD TABLE
 * ============================================================================
 */

static PyMethodDef BasicsMethods[] = {
    /* Basic functions */
    {"hello_world", hello_world, METH_VARARGS,
     "Return a hello world string.\n\nReturns:\n    str: Greeting message"},

    {"greet_name", greet_name, METH_VARARGS,
     "Greet a person by name.\n\nArgs:\n    name (str): Person's name\n\n"
     "Returns:\n    str: Personalized greeting"},

    /* Numeric operations */
    {"add_numbers", add_numbers, METH_VARARGS,
     "Add two integers.\n\nArgs:\n    a (int): First number\n    b (int): "
     "Second number\n\nReturns:\n    int: Sum of a and b"},

    {"multiply_floats", multiply_floats, METH_VARARGS,
     "Multiply two floats.\n\nArgs:\n    a (float): First number\n    b "
     "(float): Second number\n\nReturns:\n    float: Product of a and b"},

    {"divide_safe", divide_safe, METH_VARARGS,
     "Safely divide two numbers.\n\nArgs:\n    a (float): Numerator\n    b "
     "(float): Denominator\n\nReturns:\n    float: a / b\n\nRaises:\n    "
     "ZeroDivisionError: If b is zero"},

    /* Type checking */
    {"is_even", is_even, METH_VARARGS,
     "Check if a number is even.\n\nArgs:\n    num (int): Number to "
     "check\n\nReturns:\n    bool: True if even, False otherwise"},

    {"string_length", string_length, METH_VARARGS,
     "Get the length of a string.\n\nArgs:\n    s (str): Input "
     "string\n\nReturns:\n    int: Length of the string"},

    /* Optional arguments */
    {"power", (PyCFunction)power_func, METH_VARARGS | METH_KEYWORDS,
     "Calculate power of a number.\n\nArgs:\n    base (float): Base number\n   "
     " exponent (float, optional): Exponent (default: 2.0)\n\nReturns:\n    "
     "float: base ** exponent"},

    /* Multiple returns */
    {"divmod", divmod_operation, METH_VARARGS,
     "Perform division and modulo.\n\nArgs:\n    a (int): Dividend\n    b "
     "(int): Divisor\n\nReturns:\n    tuple: (quotient, remainder)"},

    {"get_statistics", get_statistics, METH_VARARGS,
     "Get statistics for a number.\n\nArgs:\n    value (float): Input "
     "value\n\nReturns:\n    dict: Statistics including value, square, and "
     "cube"},

    /* None handling */
    {"return_none", return_none, METH_VARARGS,
     "Return None.\n\nReturns:\n    None"},

    {"accept_optional", accept_optional, METH_VARARGS,
     "Accept an optional argument.\n\nArgs:\n    obj (optional): Any Python "
     "object\n\nReturns:\n    str: String representation or message"},

    {NULL, NULL, 0, NULL} /* Sentinel */
};

/* ============================================================================
 * MODULE INITIALIZATION
 * ============================================================================
 */

PyMODINIT_FUNC initbasics_module(void) {
  PyObject* m;

  m = Py_InitModule3("basics_module", BasicsMethods,
                     "Python 2.7 C-API Tutorial: Basics Module\n\n"
                     "This module demonstrates fundamental C-API concepts:\n"
                     "- Argument parsing\n"
                     "- Return value building\n"
                     "- Type conversions\n"
                     "- Error handling\n"
                     "- Optional arguments\n"
                     "- Multiple return values");

  if (m == NULL) return;

  /* Module constants */
  PyModule_AddIntConstant(m, "VERSION_MAJOR", 1);
  PyModule_AddIntConstant(m, "VERSION_MINOR", 0);
  PyModule_AddStringConstant(m, "AUTHOR", "C-API Tutorial");
}
