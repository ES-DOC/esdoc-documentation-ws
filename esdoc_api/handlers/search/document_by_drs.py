# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_drs.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by DRS search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db


# Query parameter names.
_PARAM_DRS_PATH = 'drsPath'

# Query parameter validation schema.
REQUEST_VALIDATION_SCHEMA = {
    _PARAM_DRS_PATH: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}

# Maximum number of DRS keys allowed ina path declaration.
_MAX_DRS_KEYS = 8

# Seperator used to delineate DRS keys.
_DRS_SEPERATOR = '/'


def decode_request(handler):
    """Decodes request parameters.

    """
    handler.drs_path = handler.get_argument(_PARAM_DRS_PATH)


def format_params(handler):
    """Formats request parameters.

    """
    handler.drs_path = handler.drs_path.upper()


def validate_params(handler):
    """Validates url request params.

    :param object: Search criteria.

    """
    if len(handler.drs_path.split(_DRS_SEPERATOR)) ==  1:
        raise ValueError("A DRS path must contain at least one element")
    if len(handler.drs_path.split(_DRS_SEPERATOR)) > _MAX_DRS_KEYS:
        msg = "A DRS path must consist of a maximum {0} keys"
        raise ValueError(msg.format(_MAX_DRS_KEYS))


def _get_drs_keys(project, drs_path):
    """Returns drs keys defined in a path.

    """
    def is_valid(key):
        return len(key) and key.upper() != project.upper()

    return filter(is_valid, drs_path.split(_DRS_SEPERATOR))


def do_search(handler):
    """Executes document search against db.

    :param handler: Request handler.

    :returns: Search result.
    :rtype: db.models.Document

    """
    # Set DRS keys.
    keys = _get_drs_keys(handler.project, handler.drs_path)

    # Yield search results.
    yield db.dao.get_document_by_drs_keys(
      handler.project,
      keys[0] if len(keys) > 0 else None,
      keys[1] if len(keys) > 1 else None,
      keys[2] if len(keys) > 2 else None,
      keys[3] if len(keys) > 3 else None,
      keys[4] if len(keys) > 4 else None,
      keys[5] if len(keys) > 5 else None,
      keys[6] if len(keys) > 6 else None,
      keys[7] if len(keys) > 7 else None
      )
