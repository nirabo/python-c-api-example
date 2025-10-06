/*
 * Python 2.7 C-API Tutorial: Exceptions Module
 *
 * This module covers exception handling:
 * - Raising standard exceptions
 * - Creating custom exceptions
 * - Exception checking and clearing
 * - Exception context and chaining
 * - Error indicators
 */

#include <Python.h>

/* Custom exception objects */
static PyObject* CustomError;
static PyObject* ValidationError;

/* ============================================================================
 * RAISING STANDARD EXCEPTIONS
 * ============================================================================
 */

static PyObject* raise_value_error(PyObject* self, PyObject* args) {
  const char* message;

  if (!PyArg_ParseTuple(args, "s", &message)) {
    return NULL;
  }

  PyErr_SetString(PyExc_ValueError, message);
  return NULL;
}

static PyObject* raise_type_error(PyObject* self, PyObject* args) {
  PyErr_SetString(PyExc_TypeError, "This function always raises TypeError");
  return NULL;
}

static PyObject* raise_runtime_error(PyObject* self, PyObject* args) {
  PyErr_Format(PyExc_RuntimeError, "Runtime error at position %d", 42);
  return NULL;
}

static PyObject* raise_index_error(PyObject* self, PyObject* args) {
  int index;

  if (!PyArg_ParseTuple(args, "i", &index)) {
    return NULL;
  }

  PyErr_Format(PyExc_IndexError, "Index %d is out of range", index);
  return NULL;
}

/* ============================================================================
 * RAISING CUSTOM EXCEPTIONS
 * ============================================================================
 */

static PyObject* raise_custom_error(PyObject* self, PyObject* args) {
  const char* message;

  if (!PyArg_ParseTuple(args, "s", &message)) {
    return NULL;
  }

  PyErr_SetString(CustomError, message);
  return NULL;
}

static PyObject* raise_validation_error(PyObject* self, PyObject* args) {
  const char* field;
  const char* reason;

  if (!PyArg_ParseTuple(args, "ss", &field, &reason)) {
    return NULL;
  }

  PyErr_Format(ValidationError, "Validation failed for '%s': %s", field,
               reason);
  return NULL;
}

/* ============================================================================
 * EXCEPTION CHECKING AND CLEARING
 * ============================================================================
 */

static PyObject* check_and_clear_error(PyObject* self, PyObject* args) {
  PyObject* callable;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "O", &callable)) {
    return NULL;
  }

  /* Call the object */
  result = PyObject_CallObject(callable, NULL);

  /* Check if an exception occurred */
  if (result == NULL) {
    if (PyErr_Occurred()) {
      /* Clear the exception */
      PyErr_Clear();
      return PyString_FromString("Exception was caught and cleared");
    }
  }

  Py_XDECREF(result);
  return PyString_FromString("No exception occurred");
}

static PyObject* check_exception_type(PyObject* self, PyObject* args) {
  PyObject* callable;
  PyObject* result;
  PyObject* response;

  if (!PyArg_ParseTuple(args, "O", &callable)) {
    return NULL;
  }

  result = PyObject_CallObject(callable, NULL);

  if (result == NULL) {
    if (PyErr_ExceptionMatches(PyExc_ValueError)) {
      PyErr_Clear();
      response = PyString_FromString("ValueError caught");
    } else if (PyErr_ExceptionMatches(PyExc_TypeError)) {
      PyErr_Clear();
      response = PyString_FromString("TypeError caught");
    } else {
      PyErr_Clear();
      response = PyString_FromString("Other exception caught");
    }
  } else {
    Py_DECREF(result);
    response = PyString_FromString("No exception");
  }

  return response;
}

/* ============================================================================
 * EXCEPTION CONTEXT
 * ============================================================================
 */

static PyObject* get_exception_info(PyObject* self, PyObject* args) {
  PyObject* callable;
  PyObject* result;
  PyObject *exc_type, *exc_value, *exc_traceback;
  PyObject* info_dict;

  if (!PyArg_ParseTuple(args, "O", &callable)) {
    return NULL;
  }

  result = PyObject_CallObject(callable, NULL);

  if (result == NULL) {
    /* Fetch exception info */
    PyErr_Fetch(&exc_type, &exc_value, &exc_traceback);

    info_dict = PyDict_New();

    if (exc_type != NULL) {
      PyDict_SetItemString(info_dict, "type", PyObject_Str(exc_type));
      Py_DECREF(exc_type);
    }

    if (exc_value != NULL) {
      PyDict_SetItemString(info_dict, "value", PyObject_Str(exc_value));
      Py_DECREF(exc_value);
    }

    PyDict_SetItemString(info_dict, "has_traceback",
                         PyBool_FromLong(exc_traceback != NULL));

    Py_XDECREF(exc_traceback);

    return info_dict;
  }

  Py_DECREF(result);
  Py_RETURN_NONE;
}

/* ============================================================================
 * EXCEPTION PROPAGATION
 * ============================================================================
 */

static PyObject* safe_divide(PyObject* self, PyObject* args) {
  double a, b;

  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL; /* Propagate parsing error */
  }

  if (b == 0.0) {
    PyErr_SetString(PyExc_ZeroDivisionError, "Cannot divide by zero");
    return NULL;
  }

  return PyFloat_FromDouble(a / b);
}

static PyObject* nested_call_demo(PyObject* self, PyObject* args) {
  PyObject* result;
  PyObject* divide_args;

  /* Create arguments for safe_divide */
  divide_args = Py_BuildValue("(dd)", 10.0, 0.0);

  /* This will raise an exception */
  result = safe_divide(self, divide_args);
  Py_DECREF(divide_args);

  /* If safe_divide raised an exception, it will be propagated */
  if (result == NULL) {
    return NULL;
  }

  Py_DECREF(result);
  Py_RETURN_NONE;
}

/* ============================================================================
 * ERROR INDICATORS
 * ============================================================================
 */

static PyObject* check_error_occurred(PyObject* self, PyObject* args) {
  if (PyErr_Occurred()) {
    Py_RETURN_TRUE;
  } else {
    Py_RETURN_FALSE;
  }
}

static PyObject* set_and_check(PyObject* self, PyObject* args) {
  PyObject* dict;

  dict = PyDict_New();

  /* Set an error */
  PyErr_SetString(PyExc_RuntimeError, "Test error");

  /* Check if error is set */
  if (PyErr_Occurred()) {
    Py_DECREF(dict);
    return NULL; /* Propagate the error */
  }

  return dict;
}

/* ============================================================================
 * WARNINGS
 * ============================================================================
 */

static PyObject* issue_warning(PyObject* self, PyObject* args) {
  const char* message;

  if (!PyArg_ParseTuple(args, "s", &message)) {
    return NULL;
  }

  /* Issue a deprecation warning */
  if (PyErr_WarnEx(PyExc_DeprecationWarning, message, 1) < 0) {
    return NULL;
  }

  Py_RETURN_NONE;
}

/* ============================================================================
 * MODULE METHOD TABLE
 * ============================================================================
 */

static PyMethodDef ExceptionsMethods[] = {
    /* Raising standard exceptions */
    {"raise_value_error", raise_value_error, METH_VARARGS,
     "Raise ValueError with custom message.\n\nArgs:\n    message (str): Error "
     "message\n\nRaises:\n    ValueError"},

    {"raise_type_error", raise_type_error, METH_VARARGS,
     "Always raise TypeError.\n\nRaises:\n    TypeError"},

    {"raise_runtime_error", raise_runtime_error, METH_VARARGS,
     "Raise RuntimeError with formatted message.\n\nRaises:\n    "
     "RuntimeError"},

    {"raise_index_error", raise_index_error, METH_VARARGS,
     "Raise IndexError.\n\nArgs:\n    index (int): Invalid "
     "index\n\nRaises:\n    IndexError"},

    /* Custom exceptions */
    {"raise_custom_error", raise_custom_error, METH_VARARGS,
     "Raise custom exception.\n\nArgs:\n    message (str): Error "
     "message\n\nRaises:\n    CustomError"},

    {"raise_validation_error", raise_validation_error, METH_VARARGS,
     "Raise validation error.\n\nArgs:\n    field (str): Field name\n    "
     "reason (str): Validation reason\n\nRaises:\n    ValidationError"},

    /* Exception handling */
    {"check_and_clear", check_and_clear_error, METH_VARARGS,
     "Call callable and clear any exception.\n\nArgs:\n    callable: Function "
     "to call\n\nReturns:\n    str: Result message"},

    {"check_exception_type", check_exception_type, METH_VARARGS,
     "Call callable and identify exception type.\n\nArgs:\n    callable: "
     "Function to call\n\nReturns:\n    str: Exception type name"},

    {"get_exception_info", get_exception_info, METH_VARARGS,
     "Get exception information.\n\nArgs:\n    callable: Function to "
     "call\n\nReturns:\n    dict: Exception info or None"},

    /* Exception propagation */
    {"safe_divide", safe_divide, METH_VARARGS,
     "Safely divide two numbers.\n\nArgs:\n    a (float): Numerator\n    b "
     "(float): Denominator\n\nReturns:\n    float: Result\n\nRaises:\n    "
     "ZeroDivisionError"},

    {"nested_call_demo", nested_call_demo, METH_VARARGS,
     "Demonstrate exception propagation through nested "
     "calls.\n\nRaises:\n    ZeroDivisionError"},

    /* Error indicators */
    {"check_error_occurred", check_error_occurred, METH_VARARGS,
     "Check if an error is currently set.\n\nReturns:\n    bool: True if error "
     "occurred"},

    {"set_and_check", set_and_check, METH_VARARGS,
     "Set error and check.\n\nRaises:\n    RuntimeError"},

    /* Warnings */
    {"issue_warning", issue_warning, METH_VARARGS,
     "Issue a deprecation warning.\n\nArgs:\n    message (str): Warning "
     "message\n\nReturns:\n    None"},

    {NULL, NULL, 0, NULL}};

/* ============================================================================
 * MODULE INITIALIZATION
 * ============================================================================
 */

PyMODINIT_FUNC initexceptions_module(void) {
  PyObject* m;

  m = Py_InitModule3("exceptions_module", ExceptionsMethods,
                     "Python 2.7 C-API Tutorial: Exceptions Module\n\n"
                     "This module demonstrates:\n"
                     "- Raising standard exceptions\n"
                     "- Custom exception types\n"
                     "- Exception checking and clearing\n"
                     "- Exception propagation\n"
                     "- Error indicators and warnings");

  if (m == NULL) return;

  /* Create custom exceptions */
  CustomError = PyErr_NewException("exceptions_module.CustomError", NULL, NULL);
  Py_INCREF(CustomError);
  PyModule_AddObject(m, "CustomError", CustomError);

  ValidationError =
      PyErr_NewException("exceptions_module.ValidationError", NULL, NULL);
  Py_INCREF(ValidationError);
  PyModule_AddObject(m, "ValidationError", ValidationError);
}
