# -*- coding: utf-8 -*-

"""
.. module:: url_parser.py

   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of url parsing related utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import inspect

from esdoc_api import db
from esdoc_api.utils import convert



# Map of text to boolean conversions.
_BOOLEAN_MAP = {
    'true': True,
    'True': True,
    'false': False,
    'False': False
}


def _validate_whitelisted_param(name, value, white_list):
    """Validates request parameter is a white-list member."""
    if value not in white_list:
        print value
        print white_list

        msg = "Request parameter {0}: is not in white-list.".format(name)
        raise ValueError(msg)


def _get_param_value(handler, name, info):
    """Returns value of a parameter."""
    value = handler.get_argument(name) \
            if name in handler.request.arguments else None
    if value:
        value = value.strip()
        if 'value_formatter' in info:
            value = info['value_formatter'](value)
        if value in _BOOLEAN_MAP:
            value = _BOOLEAN_MAP[value]

    return value


def _get_param_white_list(info):
    """Returns parameter white list."""
    if 'model_type' in info:
        return db.cache.get_names(info['model_type'])
    elif 'whitelist' in info:
        if inspect.isfunction(info['whitelist']):
            return info['whitelist']()
        else:
            return info['whitelist']
    else:
        return []


def _parse_param(handler, name, info):
    """Parses a request parameter."""
    # Unpack value.
    value = _get_param_value(handler, name, info)

    # Validate required.
    if info['required']:
        if value is None:
            msg = "Request parameter {0}: is mandatory.".format(name)
            raise ValueError(msg)
        if len(value) == 0:
            msg = "Request parameter {0}: is null.".format(name)
            raise ValueError(msg)

    # Validate whitelist.
    if value:
        white_list = _get_param_white_list(info)
        if white_list and value not in white_list:
            print value
            print white_list
            msg = "Request parameter {0}: is not in white-list.".format(name)
            raise ValueError(msg)

    # Set value to domain model.
    if value and 'model_type' in info:
        value = db.cache.get(info['model_type'], value)

    info['value'] = value


def parse(handler, params, apply_whitelist=True):
    """Parses incoming request url.

    :param tornado.web.RequestHAndler handler: A request handler.
    :param dict params: A request parameter validation specification.
    :param bool apply_whitelist: Flag indicating whether to apply parameter whitelist validation.

    """
    # Apply request parameters name whitelist.
    if apply_whitelist:
        for name in handler.request.arguments:
            if name not in params:
                msg = "Request parameter {0}: is unacceptable.".format(name)
                raise ValueError(msg)

    # Iterate parameters:
    for name, info in params.iteritems():
        # ... parse
        _parse_param(handler, name, info)

        # ... assign
        setattr(handler, convert.str_to_underscore_case(name), info['value'])
