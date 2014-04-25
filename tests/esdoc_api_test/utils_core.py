"""
.. module:: utils_core.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Set of test utility functions.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""
# Module imports.
import ConfigParser
import datetime
import os
import random
import uuid
from dateutil import parser as dateutil_parser
from lxml import etree as et

from nose.tools import nottest

import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session



# Integer assertion constants.
COMPARE_EXACT = "EXACT"
COMPARE_GT = "GT"
COMPARE_GTE = "GTE"
COMPARE_LTE = "LTE"
COMPARE_LT = "LT"
COMPARE_TYPES = (
    COMPARE_EXACT,
    COMPARE_GT,
    COMPARE_GTE,
    COMPARE_LT,
    COMPARE_LTE
)


# Config constants.
_CONFIG_FILENAME = "config.ini"
_CONFIG_SECTION = "prodiguer_shared_tests"
_CONFIG_ITEM_REPO_URL = "repo.url"


# Initialise config.
_cfg = ConfigParser.ConfigParser()
_cfg.read(os.path.dirname(os.path.abspath(__file__)) + "/" + _CONFIG_FILENAME)






@nottest
def get_test_file_path(ontology_name, ontology_version, file_name):
    """Returns file path for a test file.

    :param ontology_name: Ontology name.
    :type ontology_name: str

    :param ontology_version: Ontology version.
    :type ontology_version: str

    :param file_name: Name of file being tested.
    :type file_name: str

    :returns: Test file path.
    :rtype: str

    """
    path = os.path.dirname(os.path.abspath(__file__))
    path += "/files"
    path += "/" + ontology_name
    path += "/" + ontology_version
    path += "/" + file_name

    return path


@nottest
def get_test_file(ontology_name, ontology_version, file_name, type='xml'):
    """Opens & returns a test file.

    :param ontology_name: Ontology name.
    :type ontology_name: str

    :param ontology_version: Ontology version.
    :type ontology_version: str

    :param name: Name of file being tested.
    :type name: str

    :param type: Type of file being tested.
    :type type: str

    :returns: Opened file.
    :rtype: file

    """
    path = get_test_file_path(ontology_name, ontology_version, file_name)
    if type=='xml':
        return et.parse(path)
    else:
        return open(path, 'r')


def start_repo_session():
    """Starts a repo session.

    """
    session.start(_cfg.get(_CONFIG_SECTION, _CONFIG_ITEM_REPO_URL))


def end_repo_session():
    """Ends a repo session.

    """
    session.end()


def get_boolean():
    """Returns a random boolean for testing purposes.

    """
    return True


def get_date():
    """Returns a random integer for testing purposes.

    """
    return datetime.datetime.now()


def get_int(lower=0, upper=9999999):
    """Returns a random integer for testing purposes.

    """
    return random.randint(lower, upper)


def get_float():
    """Returns a random float for testing purposes.
    
    """
    return random.random()


def get_string(len):
    """Returns a random string for testing purposes.

    """
    return str(uuid.uuid1())[:len]


def get_unicode(len):
    """Returns a random unicode for testing purposes.

    """
    return unicode(uuid.uuid1())[:len]


def get_uuid():
    """Returns a uuid for testing purposes.

    """
    return str(uuid.uuid1())


def assert_iter(collection, 
                      length = -1,
                      length_compare = COMPARE_GTE,
                      item_type=None):
    """Asserts an object collection.

    :param collection: An object collection.
    :type collection: list

    :param length: Collection size.
    :type length: int

    :param length: Collection size comparason operator.
    :type length: str

    :param item_type: Type that each collection item should sub-class.
    :type item_type: class or None

    """
    assert_object(collection)
    assert iter(collection) is not None
    if length != -1:
        assert_int(len(collection), length, length_compare)
    if item_type is not None:
        if isinstance(collection, dict):
            collection = collection.values()
        for instance in collection:
            assert_object(instance, item_type)


def assert_in_collection(collection, item_attr, items):
    """Asserts an item is within a collection.

    :param collection: A collection.
    :type collection: list

    :param item: A collection item.
    :type item: object

    """
    try:
        iter(items)
    except:
        items = [items]
    targets = None
    if item_attr is not None:
        targets = [getattr(i, item_attr) for i in collection]
    else:
        targets = collection
    for item in items:
        assert item in targets, item


def assert_entity(actual, expected):
    """Asserts a pair of entity instances.

    :param actual: An entity.
    :type actual: esdoc_api.models.Entity

    :param expected: An entity.
    :type expected: esdoc_api.models.Entity

    """
    assert_object(actual, models.Entity)
    assert_object(expected, models.Entity)
    assert_int(actual.ID, expected.ID)


def assert_none(instance):
    """Asserts an instance is none.

    :param instance: An object for testing.
    :type instance: object

    """
    assert instance is None


def assert_object(instance, type=None):
    """Asserts an object instance.

    :param instance: An object for testing.
    :type instance: object

    :param type: Type that object must either be or sub-class from.
    :type type: class

    """
    assert instance is not None
    if type is not None:
        assert isinstance(instance, type)


def assert_objects(instance1, instance2):
    """Asserts that 2 object instances are equal.

    :param instance1: An object for testing.
    :type instance1: object

    :param instance2: An object for testing.
    :type instance2: object

    """
    assert instance1 is not None
    assert instance2 is not None
    assert instance1 == instance2


def assert_str(actual, expected, startswith=False):
    """Asserts a string.

    :param actual: A string.
    :type actual: str

    :param expected: Expected string value.
    :type expected: str

    :param expected: Flag indicating whether to perform startswith test.
    :type expected: bool

    """
    # Format.
    actual = str(actual).strip()
    expected = str(expected).strip()

    # Assert.
    if startswith == False:
        assert actual == expected, \
               "String mismatch : actual = {0} :: expected = {1}".format(actual, expected)
    else:
        assert actual.startswith(expected), \
               "String startswith mismatch : actual = {0} :: expected = {1}".format(actual, expected)


def assert_unicode(actual, expected):
    """Asserts a unicode.

    :param actual: A unicode.
    :type actual: str

    :param expected: Expected unicode value.
    :type expected: str

    """
    assert_object(actual, unicode)
    assert_object(expected, unicode)
    assert actual == expected, \
           "Unicode mismatch : actual = {0} :: expected = {1}".format(actual, expected)


def assert_date(actual, expected):
    """Asserts a datetime.

    :param actual: A date.
    :type actual: str

    :param expected: Expected date value.
    :type expected: str

    """
    assert actual == dateutil_parser.parse(expected)


def assert_int(actual, expected, assert_type=COMPARE_EXACT):
    """Asserts an integer.

    :param actual: An integer.
    :type actual: int

    :param expected: Expected integer value.
    :type expected: int

    """
    if assert_type == COMPARE_EXACT:
        assert actual == expected, "{0} != {1}".format(actual, expected)
    elif assert_type == COMPARE_GT:
        assert actual > expected, "{0} !> {1}".format(actual, expected)
    elif assert_type == COMPARE_GTE:
        assert actual >= expected, "{0} !>= {1}".format(actual, expected)
    elif assert_type == COMPARE_LE:
        assert actual < expected, "{0} !< {1}".format(actual, expected)
    elif assert_type == COMPARE_LTE:
        assert actual <= expected, "{0} !<= {1}".format(actual, expected)
    else:
        assert actual == expected, "{0} != {1}".format(actual, expected)


def assert_int_negative(actual, expected):
    """Negatively asserts an integer.

    :param actual: An integer.
    :type actual: int

    :param expected: Another integer value.
    :type expected: int

    """
    assert actual != expected


def assert_uuid(actual, expected):
    """Asserts a uuid.

    :param actual: A date.
    :type actual: str

    :param expected: Expected uuid value.
    :type expected: str

    """
    if isinstance(actual, uuid.UUID) == False:
        actual = uuid.UUID(actual)
    if isinstance(expected, uuid.UUID) == False:
        expected = uuid.UUID(expected)

    assert actual == expected


def assert_model_creation(type, factory):
    """Performs set of entity creation tests.

    :param type: Type of entity being tested.
    :type type: class

    """
    # Create instance directly.
    x = type()
    assert_object(x, type)
    assert_object(x, Entity)

    # Create instance via factory.
    y = factory(type)
    assert_object(y, type)
    assert_object(y, Entity)

    # Reset context.
    delete_test_models()


def assert_model_conversion(type, factory):
    """Performs set of entity conversion tests.

    :param type: Type of entity being tested.
    :type type: class

    """
    # Create instance via factory.
    x = factory(type)
    assert_object(x, type)

    # Convert to string.
    assert models.EntityConvertor.to_string(x) is not None

    # Convert to dictionary.
    assert models.EntityConvertor.to_dict(x) is not None

    # Convert to json.
    assert models.EntityConvertor.to_json(x) is not None

    # Reset context.
    delete_test_models()


def assert_model_persistence(type, factory):
    """Performs set of entity persistence tests.

    :param type: Type of entity being tested.
    :type type: class

    """
    # Cache current count.
    count = dao.get_count(type)

    # Create instance via factory.
    factory(type)

    # Reassert counts.
    assert_int(dao.get_count(type), count + 1)

    # Delete & reassert count.
    delete_test_models()
    assert_int(dao.get_count(type), count)
