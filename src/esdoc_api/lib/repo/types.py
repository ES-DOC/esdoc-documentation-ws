"""Manages set of domain types to be exposed to http.

"""

# Module imports.
from esdoc_api.models import *
from esdoc_api.lib.repo.search import *


# Managed collection of types being exposed to http.
_types = {}


def _register_type(type):
    """Registers a type to be exposed to http.

    :param type: Type being registered.
    :type type: subclass of either models.core.ESDOCEntity or models.core.CIMSearch

    """
    _types[type.__name__.upper()] = type


# Register search types.
_register_type(S1Search)


def get_type(type_name):
    """Registers an entity type.

    :param type_name: Name of a registered type.
    :type type_name: str

    :returns: A registered type.
    :rtype: 

    """
    try:
        return _types[type_name.upper()]
    except KeyError:
        print "Type name is unsupported :: {0}.".format(type_name)

