/*
 * Python 2.7 C-API Tutorial: Memory Management Module
 *
 * This module covers memory management:
 * - Reference counting (Py_INCREF, Py_DECREF)
 * - Memory allocation (PyMem_Malloc, PyMem_Free)
 * - Object creation and destruction
 * - Memory leak prevention
 * - Borrowed vs owned references
 */

#include <Python.h>
#include <string.h>

/* ============================================================================
 * REFERENCE COUNTING DEMONSTRATIONS
 * ============================================================================
 */

static PyObject* get_refcount(PyObject* self, PyObject* args) {
  PyObject* obj;

  if (!PyArg_ParseTuple(args, "O", &obj)) {
    return NULL;
  }

  return PyInt_FromSsize_t(obj->ob_refcnt);
}

static PyObject* incref_demo(PyObject* self, PyObject* args) {
  PyObject* obj;
  Py_ssize_t before, after;

  if (!PyArg_ParseTuple(args, "O", &obj)) {
    return NULL;
  }

  before = obj->ob_refcnt;
  Py_INCREF(obj);
  after = obj->ob_refcnt;
  Py_DECREF(obj); /* Restore original count */

  return Py_BuildValue("(nn)", before, after);
}

static PyObject* create_temp_list(PyObject* self, PyObject* args) {
  int size, i;
  PyObject* list;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "i", &size)) {
    return NULL;
  }

  /* Create a temporary list */
  list = PyList_New(size);
  if (list == NULL) {
    return NULL;
  }

  for (i = 0; i < size; i++) {
    PyObject* item = PyInt_FromLong(i);
    PyList_SET_ITEM(list, i, item); /* Steals reference */
  }

  /* Get length and then destroy list */
  result = PyInt_FromSsize_t(PyList_Size(list));

  /* Properly decrement reference */
  Py_DECREF(list);

  return result;
}

/* ============================================================================
 * MEMORY ALLOCATION
 * ============================================================================
 */

static PyObject* allocate_buffer(PyObject* self, PyObject* args) {
  int size;
  char* buffer;
  PyObject* result;
  int i;

  if (!PyArg_ParseTuple(args, "i", &size)) {
    return NULL;
  }

  /* Allocate memory using Python's allocator */
  buffer = (char*)PyMem_Malloc(size * sizeof(char));
  if (buffer == NULL) {
    return PyErr_NoMemory();
  }

  /* Fill buffer */
  for (i = 0; i < size; i++) {
    buffer[i] = 'A' + (i % 26);
  }

  /* Create Python string from buffer */
  result = PyString_FromStringAndSize(buffer, size);

  /* Free the allocated memory */
  PyMem_Free(buffer);

  return result;
}

static PyObject* copy_string_safe(PyObject* self, PyObject* args) {
  const char* input;
  int input_len;

  /* Parse string argument - let Python handle the length */
  if (!PyArg_ParseTuple(args, "s", &input)) {
    return NULL;
  }

  /* Calculate length */
  input_len = strlen(input);

  /* Allocate buffer for copy */
  char* buffer = (char*)PyMem_Malloc((input_len + 1) * sizeof(char));
  if (buffer == NULL) {
    return PyErr_NoMemory();
  }

  /* Copy the string */
  strcpy(buffer, input);

  /* Create Python string from copied buffer */
  PyObject* result = PyString_FromString(buffer);

  /* Free the buffer */
  PyMem_Free(buffer);

  return result;
}

/* ============================================================================
 * BORROWED VS OWNED REFERENCES
 * ============================================================================
 */

static PyObject* borrowed_reference_demo(PyObject* self, PyObject* args) {
  PyObject* list;
  PyObject* item;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)) {
    return NULL;
  }

  if (PyList_Size(list) == 0) {
    PyErr_SetString(PyExc_ValueError, "list is empty");
    return NULL;
  }

  /* PyList_GetItem returns a BORROWED reference */
  item = PyList_GetItem(list, 0);
  if (item == NULL) {
    return NULL;
  }

  /* Must INCREF if we want to keep it */
  Py_INCREF(item);

  /* Create result dict */
  result = PyDict_New();
  PyDict_SetItemString(result, "item", item);
  PyDict_SetItemString(result, "refcount", PyInt_FromSsize_t(item->ob_refcnt));

  /* DECREF our reference */
  Py_DECREF(item);

  return result;
}

static PyObject* owned_reference_demo(PyObject* self, PyObject* args) {
  int value;
  PyObject* new_int;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "i", &value)) {
    return NULL;
  }

  /* PyInt_FromLong returns a NEW (owned) reference */
  new_int = PyInt_FromLong(value);
  if (new_int == NULL) {
    return NULL;
  }

  /* Create result */
  result = PyDict_New();
  PyDict_SetItemString(result, "value", new_int);
  PyDict_SetItemString(result, "refcount",
                       PyInt_FromSsize_t(new_int->ob_refcnt));

  /* We own the reference, so we must DECREF it */
  Py_DECREF(new_int);

  return result;
}

/* ============================================================================
 * MEMORY LEAK PREVENTION
 * ============================================================================
 */

static PyObject* proper_cleanup_demo(PyObject* self, PyObject* args) {
  const char* str1;
  const char* str2;
  char* buffer = NULL;
  PyObject* result = NULL;
  size_t len1, len2, total_len;

  if (!PyArg_ParseTuple(args, "ss", &str1, &str2)) {
    return NULL;
  }

  len1 = strlen(str1);
  len2 = strlen(str2);
  total_len = len1 + len2 + 2; /* +2 for space and null terminator */

  /* Allocate buffer */
  buffer = (char*)PyMem_Malloc(total_len);
  if (buffer == NULL) {
    return PyErr_NoMemory();
  }

  /* Concatenate strings */
  strcpy(buffer, str1);
  strcat(buffer, " ");
  strcat(buffer, str2);

  /* Create Python string */
  result = PyString_FromString(buffer);

  /* Always cleanup, even if PyString_FromString failed */
  PyMem_Free(buffer);

  /* result might be NULL if PyString_FromString failed */
  return result;
}

static PyObject* exception_safe_demo(PyObject* self, PyObject* args) {
  PyObject* list = NULL;
  PyObject* item = NULL;
  PyObject* result = NULL;
  int i;

  list = PyList_New(0);
  if (list == NULL) {
    goto error;
  }

  for (i = 0; i < 10; i++) {
    item = PyInt_FromLong(i * i);
    if (item == NULL) {
      goto error;
    }

    if (PyList_Append(list, item) < 0) {
      Py_DECREF(item);
      goto error;
    }

    Py_DECREF(item); /* Append incremented ref count */
    item = NULL;
  }

  result = list;
  list = NULL;

error:
  Py_XDECREF(list);
  Py_XDECREF(item);
  return result;
}

/* ============================================================================
 * OBJECT LIFECYCLE
 * ============================================================================
 */

static PyObject* create_and_populate_dict(PyObject* self, PyObject* args) {
  int count;
  PyObject* dict = NULL;
  PyObject* key = NULL;
  PyObject* value = NULL;
  int i;

  if (!PyArg_ParseTuple(args, "i", &count)) {
    return NULL;
  }

  dict = PyDict_New();
  if (dict == NULL) {
    return NULL;
  }

  for (i = 0; i < count; i++) {
    key = PyString_FromFormat("key_%d", i);
    if (key == NULL) {
      Py_DECREF(dict);
      return NULL;
    }

    value = PyInt_FromLong(i * 100);
    if (value == NULL) {
      Py_DECREF(key);
      Py_DECREF(dict);
      return NULL;
    }

    /* PyDict_SetItem increments refcounts of key and value */
    if (PyDict_SetItem(dict, key, value) < 0) {
      Py_DECREF(key);
      Py_DECREF(value);
      Py_DECREF(dict);
      return NULL;
    }

    /* We must decrement our references */
    Py_DECREF(key);
    Py_DECREF(value);
  }

  return dict;
}

/* ============================================================================
 * MODULE METHOD TABLE
 * ============================================================================
 */

static PyMethodDef MemoryMethods[] = {
    /* Reference counting */
    {"get_refcount", get_refcount, METH_VARARGS,
     "Get reference count of an object.\n\nArgs:\n    obj: Any Python "
     "object\n\nReturns:\n    int: Current reference count"},

    {"incref_demo", incref_demo, METH_VARARGS,
     "Demonstrate INCREF/DECREF.\n\nArgs:\n    obj: Any Python "
     "object\n\nReturns:\n    tuple: (before_count, after_count)"},

    {"create_temp_list", create_temp_list, METH_VARARGS,
     "Create temporary list and clean up.\n\nArgs:\n    size (int): List "
     "size\n\nReturns:\n    int: Size of temporary list"},

    /* Memory allocation */
    {"allocate_buffer", allocate_buffer, METH_VARARGS,
     "Allocate and fill a buffer.\n\nArgs:\n    size (int): Buffer "
     "size\n\nReturns:\n    str: String filled with pattern"},

    {"copy_string", copy_string_safe, METH_VARARGS,
     "Safely copy a string using PyMem_Malloc.\n\nArgs:\n    s (str): Input "
     "string\n\nReturns:\n    str: Copied string"},

    /* Borrowed vs owned */
    {"borrowed_ref_demo", borrowed_reference_demo, METH_VARARGS,
     "Demonstrate borrowed references.\n\nArgs:\n    lst (list): Non-empty "
     "list\n\nReturns:\n    dict: Info about first element"},

    {"owned_ref_demo", owned_reference_demo, METH_VARARGS,
     "Demonstrate owned references.\n\nArgs:\n    value (int): Integer "
     "value\n\nReturns:\n    dict: Info about new object"},

    /* Memory safety */
    {"proper_cleanup", proper_cleanup_demo, METH_VARARGS,
     "Demonstrate proper cleanup.\n\nArgs:\n    str1 (str): First string\n    "
     "str2 (str): Second string\n\nReturns:\n    str: Concatenated string"},

    {"exception_safe", exception_safe_demo, METH_VARARGS,
     "Create list with exception safety.\n\nReturns:\n    list: List of "
     "squares"},

    {"create_populated_dict", create_and_populate_dict, METH_VARARGS,
     "Create and populate dictionary safely.\n\nArgs:\n    count (int): Number "
     "of entries\n\nReturns:\n    dict: Populated dictionary"},

    {NULL, NULL, 0, NULL}};

/* ============================================================================
 * MODULE INITIALIZATION
 * ============================================================================
 */

PyMODINIT_FUNC initmemory_module(void) {
  PyObject* m;

  m = Py_InitModule3("memory_module", MemoryMethods,
                     "Python 2.7 C-API Tutorial: Memory Management Module\n\n"
                     "This module demonstrates:\n"
                     "- Reference counting (INCREF/DECREF)\n"
                     "- Memory allocation (PyMem_Malloc/Free)\n"
                     "- Borrowed vs owned references\n"
                     "- Memory leak prevention\n"
                     "- Exception-safe code");

  if (m == NULL) return;
}
