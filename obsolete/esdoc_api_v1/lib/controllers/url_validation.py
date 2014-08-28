"""
.. module:: esdoc_api.lib.controllers.validation.py
   :copyright: Copyright "Jul 31, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of url validation related utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from pylons import request
from pylons.controllers.util import abort

from esdoc_api.lib.utils.http_utils import HTTP_RESPONSE_BAD_REQUEST



def _abort(msg):
    """Helper function to abort request processing."""
    abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def _exists(name):
    """Validates query url parameter existence."""
    if not request.params.has_key(name):
        _abort("URL query parameter {0} is unspecified.".format(name))


def _not_null(name):
    """Validates query url parameter nullness."""
    if not request.params[name].strip():
        _abort("URL query parameter {0} is undefined.".format(name))


def _not_other(names):
    """Validates presence of a set of query url parameters."""
    for name in request.params:
        if name not in names:
            msg = "URL query parameter {0} is unacceptable.".format(name)
            abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def _is_in(name, white_list, key_formatter=None):
    """Validates that a query url parameter is a members of the passed white list."""
    key = request.params[name] if key_formatter is None else key_formatter(request.params[name])
    if key not in white_list:
        msg = "URL query parameter {0} value ({1}) is unsupported.".format(name, request.params[name])
        abort(HTTP_RESPONSE_BAD_REQUEST, msg)


def _validate_param(param):
    """Validate a parameter."""
    # Validate required parameters.
    if param['required'] == True:
        _exists(param['name'])
        _not_null(param['name'])

    # Validate whitelists.
    if request.params.has_key(param['name']) and param.has_key('whitelist'):
        _is_in(param['name'],
               param['whitelist'](),
               param['key_formatter'] if param.has_key('key_formatter') else None)


def _validate_params(params):
    """Validate set of parameters."""
    # Validate param name whitelist.
    _not_other(map(lambda p : p['name'], params))

    # Validate individual params.
    for param in params:
        _validate_param(param)


def validate(spec):
    """Validates request against a url parameter validation specification.

    :param spec: A url parameter validation specification.
    :type spec: dict or list

    """
    if isinstance(spec, dict):
        _validate_param(spec)
    else:
        _validate_params(spec)
