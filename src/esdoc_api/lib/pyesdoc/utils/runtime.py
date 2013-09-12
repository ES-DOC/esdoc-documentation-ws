"""
.. module:: esdoc_api.lib.pyesdoc.utils.runtime.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Runtime utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import inspect



class PYESDOC_Exception(Exception):
    """Default library exception class.

    """

    def __init__(self, msg):
        """Contructor.

        :param msg: Exception message.
        :type msg: str

        """
        self.message = msg() if inspect.isfunction(msg) else str(msg)


    def __str__(self):
        """Returns a string representation.

        """
        return "ES-DOC PY-CLIENT EXCEPTION : {0}".format(repr(self.message))


def raise_error(msg, type=PYESDOC_Exception):
    """Helper function to raise a runtime error.

    :param msg: Error message.
    :type msg: str

    :param type: Error type.
    :type type: class

    """
    raise type(msg)


def assert_function(f, msg=None):
    """Asserts that a variable is a function.

    :param f: Variable that should be a function pointer.
    :type f: function

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    def get_msg():
        return "Function assertion failure."

    if not inspect.isfunction(f):
        throw(get_msg if msg is None else msg)


def assert_var(name, value, type, msg=None):
    """Asserts that a variable is of the expected type.

    :param name: Variable name.
    :type name: str

    :param name: Variable value.
    :type value: object

    :param name: Variable type.
    :type type: class

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    def get_msg():
        msg = "Parameter '{0}' is of an invalid type (expected type = {1})."
        return msg.format(name, type.__name__)

    if value is None or not isinstance(value, type):
        throw(get_msg if msg is None else msg)


def assert_optional_var(name, value, type, msg=None):
    """Asserts that a variable is of the expected type if it is not None.

    :param name: Variable name.
    :type name: str

    :param name: Variable value.
    :type value: object

    :param name: Variable type.
    :type type: class

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    if value is not None:
        assert_var(name, value, type, msg)


def assert_iter_item(collection, item, msg=None):
    """Asserts that an item is a member of passed collection.

    :param collection: A collection that should contain the specified item.
    :type collection: iterable

    :param item: An item that should be a collection member.
    :type item: object

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    def get_msg():
        return "Item not found within collection :: {0}.".format(item)

    assert_iter(collection)
    if not item in collection:
        throw(get_msg if msg is None else msg)


def assert_iter(collection, msg=None):
    """Asserts that an item is a an iterable.

    :param collection: A collection that should be iterable.
    :type collection: iterable

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    def get_msg():
        return "Collection is not iterable."

    try:
        iter(collection)
    except TypeError:
        throw(get_msg if msg is None else msg)


def assert_typed_iter(collection, type, msg=None):
    """Asserts that each collection member is of the expected type.

    :param collection: A collection.
    :type collection: iterable


    :param type: Type that each collection item should sub-class.
    :type type: class or None

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    def get_msg():
        msg = "Collection contains items of an invalid type (expected type = {0})."
        return msg.format(type.__name__)

    assert_iter(collection)
    if len([i for i in collection if not isinstance(i, type)]) > 0:
        throw(get_msg if msg is None else msg)


def assert_attr(instance, attr, msg=None):
    """Asserts that passed instance has the passed attribute (i.e. is it a duck ?).

    :param instance: An object instance.
    :type item: object

    :param attr: Name of attribute that instance should contain.
    :type item: str

    :param msg: Error message to output if assertion fails.
    :type msg: str or None

    """
    def get_msg():
        return "Attribute {0} is not found.".format(attr)

    assert_var('instance', instance, object)
    if not hasattr(instance, attr):
        throw(get_msg if msg is None else msg)


def assert_doc(name, value):
    """Asserts thay passed variable is a esdoc_api.lib.pyesdoc object instance.

    :param name: Variable name.
    :type name: str

    :param value: Variable value.
    :type value: object

    """
    def get_msg():
        return "{0} is not a esdoc_api.lib.pyesdoc type instance".format(name)

    assert_var(name, value, object, msg=get_msg)
    assert_attr(value, 'doc_info', msg=get_msg)


def is_iterable(target):
    """Returns a flag indicating whether passed variable is iterable.

    :param target: Varaible being tested whether it is iterable or not.
    :type target: object or iterable

    """
    is_iterable = True
    try:
        iter(target)
    except TypeError:
        is_iterable = False

    return is_iterable


def assert_params(params, rules):
    """Performs a set of assertions over a parameter dictionary.

    :param params: Dictionary or input parameters.
    :type params: dict

    :param rules: Set of assertion rules.
    :type rules: list

    """
    for rule in rules:
        # Unpack rule.
        name, white_list = rule

        # Assert param is specified.
        if not params.has_key(name) or not len(str(params[name])):
            throw("Parameter {0} is unspecified.".format(name))

        # Assert param value is in constrained list.
        if len(white_list):
            if params[name] not in white_list:
                throw("Parameter {0} is invalid.".format(name))


def throw(msg):
    """Throws an ES-DOC API error.

    :param msg: Error message.
    :type msg: str

    """
    raise PYESDOC_Exception(msg)



def log(msg):
    """Outputs a message to log.

    :param msg: Logging message.
    :type msg: str

    """
    print "ES-DOC API :: " + str(msg)
