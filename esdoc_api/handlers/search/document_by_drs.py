# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_drs.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by DRS search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db


# Maximum number of DRS keys allowed ina path declaration.
_MAX_DRS_KEYS = 8

# Seperator used to delineate DRS keys.
_DRS_SEPERATOR = '/'


def _get_drs_keys(project, drs_path):
    """Returns drs keys defined in a path."""
    def is_valid(key):
        return len(key) and key.upper() != project.upper()

    return filter(is_valid, drs_path.split(_DRS_SEPERATOR))


def get_url_params():
    """Returns url parameter specification."""
    return {
        'drsPath': {
            'required': True,
            'value_formatter': lambda v : v.upper()
        },
    }


def parse_url_params(params):
    """Parses url request params.

    :param object: Search criteria.

    """
    if not len(params.drs_path.split(_DRS_SEPERATOR)):
        raise ValueError("A DRS path must contain at least one element")
    if len(params.drs_path.split(_DRS_SEPERATOR)) > _MAX_DRS_KEYS:
        msg = "A DRS path must consist of a maximum {0} keys"
        raise ValueError(msg.format(_MAX_DRS_KEYS))


def do_search(criteria):
    """Executes document search against db.

    :param object: Search criteria.

    :returns: Search result.
    :rtype: db.models.Document | None

    """
    keys = _get_drs_keys(criteria.project.Name, criteria.drs_path)
    yield db.dao.get_document_by_drs_keys(
      criteria.project.ID,
      keys[0] if len(keys) > 0 else None,
      keys[1] if len(keys) > 1 else None,
      keys[2] if len(keys) > 2 else None,
      keys[3] if len(keys) > 3 else None,
      keys[4] if len(keys) > 4 else None,
      keys[5] if len(keys) > 5 else None,
      keys[6] if len(keys) > 6 else None,
      keys[7] if len(keys) > 7 else None
      )
