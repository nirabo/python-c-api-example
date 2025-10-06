/*
 * Python 2.7 C-API Tutorial: Objects Module
 *
 * This module covers object manipulation:
 * - List operations
 * - Dictionary operations
 * - Tuple operations
 * - Set operations
 * - Object attribute access
 * - Type checking
 */

#include <Python.h>

/* ============================================================================
 * LIST OPERATIONS
 * ============================================================================
 */

static PyObject* create_list(PyObject* self, PyObject* args) {
  int size;
  PyObject* list;
  int i;

  if (!PyArg_ParseTuple(args, "i", &size)) {
    return NULL;
  }

  list = PyList_New(size);
  if (list == NULL) {
    return NULL;
  }

  for (i = 0; i < size; i++) {
    PyObject* item = PyInt_FromLong(i * i);
    PyList_SET_ITEM(list, i, item);
  }

  return list;
}

static PyObject* sum_list(PyObject* self, PyObject* args) {
  PyObject* list;
  Py_ssize_t i, size;
  long total = 0;

  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)) {
    return NULL;
  }

  size = PyList_Size(list);

  for (i = 0; i < size; i++) {
    PyObject* item = PyList_GetItem(list, i);
    if (!PyInt_Check(item) && !PyLong_Check(item)) {
      PyErr_SetString(PyExc_TypeError, "list must contain only integers");
      return NULL;
    }
    total += PyInt_AsLong(item);
  }

  return PyInt_FromLong(total);
}

static PyObject* reverse_list(PyObject* self, PyObject* args) {
  PyObject* list;

  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)) {
    return NULL;
  }

  if (PyList_Reverse(list) < 0) {
    return NULL;
  }

  Py_INCREF(list);
  return list;
}

/* ============================================================================
 * DICTIONARY OPERATIONS
 * ============================================================================
 */

static PyObject* create_dict(PyObject* self, PyObject* args) {
  PyObject* dict;
  int i;

  dict = PyDict_New();
  if (dict == NULL) {
    return NULL;
  }

  for (i = 0; i < 5; i++) {
    PyObject* key = PyString_FromFormat("key%d", i);
    PyObject* value = PyInt_FromLong(i * 10);
    PyDict_SetItem(dict, key, value);
    Py_DECREF(key);
    Py_DECREF(value);
  }

  return dict;
}

static PyObject* dict_has_key(PyObject* self, PyObject* args) {
  PyObject* dict;
  const char* key;

  if (!PyArg_ParseTuple(args, "O!s", &PyDict_Type, &dict, &key)) {
    return NULL;
  }

  if (PyDict_GetItemString(dict, key) != NULL) {
    Py_RETURN_TRUE;
  } else {
    Py_RETURN_FALSE;
  }
}

static PyObject* merge_dicts(PyObject* self, PyObject* args) {
  PyObject *dict1, *dict2, *result;

  if (!PyArg_ParseTuple(args, "O!O!", &PyDict_Type, &dict1, &PyDict_Type,
                        &dict2)) {
    return NULL;
  }

  result = PyDict_Copy(dict1);
  if (result == NULL) {
    return NULL;
  }

  if (PyDict_Update(result, dict2) < 0) {
    Py_DECREF(result);
    return NULL;
  }

  return result;
}

/* ============================================================================
 * TUPLE OPERATIONS
 * ============================================================================
 */

static PyObject* create_tuple(PyObject* self, PyObject* args) {
  int size;
  PyObject* tuple;
  int i;

  if (!PyArg_ParseTuple(args, "i", &size)) {
    return NULL;
  }

  tuple = PyTuple_New(size);
  if (tuple == NULL) {
    return NULL;
  }

  for (i = 0; i < size; i++) {
    PyObject* item = PyInt_FromLong(i + 1);
    PyTuple_SET_ITEM(tuple, i, item);
  }

  return tuple;
}

static PyObject* tuple_element(PyObject* self, PyObject* args) {
  PyObject* tuple;
  int index;
  PyObject* item;

  if (!PyArg_ParseTuple(args, "O!i", &PyTuple_Type, &tuple, &index)) {
    return NULL;
  }

  if (index < 0 || index >= PyTuple_Size(tuple)) {
    PyErr_SetString(PyExc_IndexError, "tuple index out of range");
    return NULL;
  }

  item = PyTuple_GetItem(tuple, index);
  Py_INCREF(item);
  return item;
}

/* ============================================================================
 * SET OPERATIONS
 * ============================================================================
 */

static PyObject* create_set(PyObject* self, PyObject* args) {
  PyObject* list;
  PyObject* set;

  if (!PyArg_ParseTuple(args, "O!", &PyList_Type, &list)) {
    return NULL;
  }

  set = PySet_New(list);
  return set;
}

static PyObject* set_operations(PyObject* self, PyObject* args) {
  PyObject *set1, *set2;
  PyObject* result;

  if (!PyArg_ParseTuple(args, "O!O!", &PySet_Type, &set1, &PySet_Type, &set2)) {
    return NULL;
  }

  /* Create union */
  result = PyNumber_Or(set1, set2);

  return result;
}

/* ============================================================================
 * OBJECT ATTRIBUTE ACCESS
 * ============================================================================
 */

static PyObject* get_object_attr(PyObject* self, PyObject* args) {
  PyObject* obj;
  const char* attr_name;
  PyObject* attr;

  if (!PyArg_ParseTuple(args, "Os", &obj, &attr_name)) {
    return NULL;
  }

  attr = PyObject_GetAttrString(obj, attr_name);
  if (attr == NULL) {
    PyErr_Clear();
    Py_RETURN_NONE;
  }

  return attr;
}

static PyObject* set_object_attr(PyObject* self, PyObject* args) {
  PyObject* obj;
  const char* attr_name;
  PyObject* value;

  if (!PyArg_ParseTuple(args, "OsO", &obj, &attr_name, &value)) {
    return NULL;
  }

  if (PyObject_SetAttrString(obj, attr_name, value) < 0) {
    return NULL;
  }

  Py_RETURN_NONE;
}

static PyObject* has_attribute(PyObject* self, PyObject* args) {
  PyObject* obj;
  const char* attr_name;

  if (!PyArg_ParseTuple(args, "Os", &obj, &attr_name)) {
    return NULL;
  }

  if (PyObject_HasAttrString(obj, attr_name)) {
    Py_RETURN_TRUE;
  } else {
    Py_RETURN_FALSE;
  }
}

/* ============================================================================
 * TYPE CHECKING
 * ============================================================================
 */

static PyObject* get_object_type(PyObject* self, PyObject* args) {
  PyObject* obj;
  const char* type_name;

  if (!PyArg_ParseTuple(args, "O", &obj)) {
    return NULL;
  }

  type_name = obj->ob_type->tp_name;
  return PyString_FromString(type_name);
}

static PyObject* check_type(PyObject* self, PyObject* args) {
  PyObject* obj;
  PyObject* dict;

  if (!PyArg_ParseTuple(args, "O", &obj)) {
    return NULL;
  }

  dict = PyDict_New();

  PyDict_SetItemString(dict, "is_int", PyBool_FromLong(PyInt_Check(obj)));
  PyDict_SetItemString(dict, "is_long", PyBool_FromLong(PyLong_Check(obj)));
  PyDict_SetItemString(dict, "is_float", PyBool_FromLong(PyFloat_Check(obj)));
  PyDict_SetItemString(dict, "is_string", PyBool_FromLong(PyString_Check(obj)));
  PyDict_SetItemString(dict, "is_unicode",
                       PyBool_FromLong(PyUnicode_Check(obj)));
  PyDict_SetItemString(dict, "is_list", PyBool_FromLong(PyList_Check(obj)));
  PyDict_SetItemString(dict, "is_tuple", PyBool_FromLong(PyTuple_Check(obj)));
  PyDict_SetItemString(dict, "is_dict", PyBool_FromLong(PyDict_Check(obj)));
  PyDict_SetItemString(dict, "is_set", PyBool_FromLong(PySet_Check(obj)));

  return dict;
}

/* ============================================================================
 * OBJECT COMPARISON
 * ============================================================================
 */

static PyObject* compare_objects(PyObject* self, PyObject* args) {
  PyObject *obj1, *obj2;
  int result;

  if (!PyArg_ParseTuple(args, "OO", &obj1, &obj2)) {
    return NULL;
  }

  result = PyObject_Compare(obj1, obj2);

  if (PyErr_Occurred()) {
    return NULL;
  }

  return PyInt_FromLong(result);
}

/* ============================================================================
 * MODULE METHOD TABLE
 * ============================================================================
 */

static PyMethodDef ObjectsMethods[] = {
    /* List operations */
    {"create_list", create_list, METH_VARARGS,
     "Create a list of squares.\n\nArgs:\n    size (int): Size of "
     "list\n\nReturns:\n    list: List of squares [0, 1, 4, 9, ...]"},

    {"sum_list", sum_list, METH_VARARGS,
     "Sum all integers in a list.\n\nArgs:\n    lst (list): List of "
     "integers\n\nReturns:\n    int: Sum of all elements"},

    {"reverse_list", reverse_list, METH_VARARGS,
     "Reverse a list in-place.\n\nArgs:\n    lst (list): List to "
     "reverse\n\nReturns:\n    list: The reversed list"},

    /* Dictionary operations */
    {"create_dict", create_dict, METH_VARARGS,
     "Create a sample dictionary.\n\nReturns:\n    dict: Dictionary with "
     "key0-key4 mapping to 0, 10, 20, 30, 40"},

    {"dict_has_key", dict_has_key, METH_VARARGS,
     "Check if dictionary has a key.\n\nArgs:\n    d (dict): Dictionary\n    "
     "key (str): Key to check\n\nReturns:\n    bool: True if key exists"},

    {"merge_dicts", merge_dicts, METH_VARARGS,
     "Merge two dictionaries.\n\nArgs:\n    dict1 (dict): First dictionary\n  "
     "  dict2 (dict): Second dictionary\n\nReturns:\n    dict: Merged "
     "dictionary"},

    /* Tuple operations */
    {"create_tuple", create_tuple, METH_VARARGS,
     "Create a tuple of integers.\n\nArgs:\n    size (int): Size of "
     "tuple\n\nReturns:\n    tuple: Tuple of integers (1, 2, 3, ...)"},

    {"tuple_element", tuple_element, METH_VARARGS,
     "Get element from tuple.\n\nArgs:\n    t (tuple): Tuple\n    index (int): "
     "Index\n\nReturns:\n    object: Element at index"},

    /* Set operations */
    {"create_set", create_set, METH_VARARGS,
     "Create a set from a list.\n\nArgs:\n    lst (list): Input "
     "list\n\nReturns:\n    set: Set containing unique elements"},

    {"set_union", set_operations, METH_VARARGS,
     "Union of two sets.\n\nArgs:\n    set1 (set): First set\n    set2 (set): "
     "Second set\n\nReturns:\n    set: Union of sets"},

    /* Attribute access */
    {"get_attr", get_object_attr, METH_VARARGS,
     "Get object attribute.\n\nArgs:\n    obj: Object\n    name (str): "
     "Attribute name\n\nReturns:\n    object: Attribute value or None"},

    {"set_attr", set_object_attr, METH_VARARGS,
     "Set object attribute.\n\nArgs:\n    obj: Object\n    name (str): "
     "Attribute name\n    value: Value to set\n\nReturns:\n    None"},

    {"has_attr", has_attribute, METH_VARARGS,
     "Check if object has attribute.\n\nArgs:\n    obj: Object\n    name "
     "(str): "
     "Attribute name\n\nReturns:\n    bool: True if attribute exists"},

    /* Type checking */
    {"get_type", get_object_type, METH_VARARGS,
     "Get object type name.\n\nArgs:\n    obj: Object\n\nReturns:\n    str: "
     "Type name"},

    {"check_type", check_type, METH_VARARGS,
     "Check object against all basic types.\n\nArgs:\n    obj: "
     "Object\n\nReturns:\n    dict: Dictionary of type checks"},

    {"compare", compare_objects, METH_VARARGS,
     "Compare two objects.\n\nArgs:\n    obj1: First object\n    obj2: Second "
     "object\n\nReturns:\n    int: -1, 0, or 1"},

    {NULL, NULL, 0, NULL}};

/* ============================================================================
 * MODULE INITIALIZATION
 * ============================================================================
 */

PyMODINIT_FUNC initobjects_module(void) {
  PyObject* m;

  m = Py_InitModule3("objects_module", ObjectsMethods,
                     "Python 2.7 C-API Tutorial: Objects Module\n\n"
                     "This module demonstrates object manipulation:\n"
                     "- List, dict, tuple, and set operations\n"
                     "- Attribute access\n"
                     "- Type checking\n"
                     "- Object comparison");

  if (m == NULL) return;
}
