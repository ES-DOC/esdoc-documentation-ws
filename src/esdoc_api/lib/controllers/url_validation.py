"""
.. module:: esdoc_api.lib.controllers.validation.py
   :copyright: Copyright "Jul 31, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of url validation related utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from pylons import request
from pylons.controllers.util import abort

from esdoc_api.lib.utils.http_utils import HTTP_RESPONSE_BAD_REQUEST
import esdoc_api.lib.utils.runtime as rt



def must_exist(name):
    """Validates that a query url parameter exists.

    :param name: Query url parameter name.
    :type name: str

    """
    if not request.params.has_key(name):
        msg = "URL query parameter {0} is unspecified.".format(name)
        abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def must_not_be_null(name):
    """Validates that a query url parameter is not null.

    :param name: Query url parameter name.
    :type name: str

    """
    if not request.params[name].strip():
        msg = "URL query parameter {0} is undefined.".format(name)
        abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def must_not_be_other(names):
    """Validates that a query url parameter is not null.

    :param name: Query url parameter name.
    :type name: str

    """
    for name in request.params:
        if name not in names:
            msg = "URL query parameter {0} is unacceptable.".format(name)
            abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def must_be_in(name, white_list, name_formatter=lambda x : x.lower()):
    """Validates that a query url parameter is a members of the passed white list.

    :param name: Query url parameter name.
    :type name: str

    :param white_list: A white list of allowed name values.
    :type white_list: list

    :param name_formatter: A name formatting function.
    :type name_formatter: function

    """
    if name_formatter(request.params[name]) not in white_list:
        msg = "URL query parameter {0} value ({1}) is unsupported.".format(name, request.params[name])
        abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def must(rules):
    """Executes a set of query url parameter validation rules.

    :param rules: A set of query url parameter validation rules.
    :type name: list

    """
    for rule in rules:
        if len(rule) == 2:
            rule[1](rule[0])
        else:
            rule[1](rule[0], rule[2])