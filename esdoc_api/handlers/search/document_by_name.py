# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_name.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by name search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db



# Query parameter names.
_PARAM_INSTITUTE = 'institute'
_PARAM_NAME = 'name'
_PARAM_TYPE = 'type'

# Query parameter validation schema.
REQUEST_VALIDATION_SCHEMA = {
    _PARAM_INSTITUTE: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_NAME: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_TYPE: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}


def decode_request(handler):
    """Decodes request parameters.

    """
    handler.institute = handler.get_argument(_PARAM_INSTITUTE)
    handler.name = handler.get_argument(_PARAM_NAME)
    handler.typeof = handler.get_argument(_PARAM_TYPE)


def do_search(handler):
    """Executes document search against db.

    :param handler: Request handler.

    :returns: Search result.
    :rtype: db.models.Document

    """
    yield db.dao.get_document_by_name(handler.project,
                                      handler.typeof,
                                      handler.name,
                                      handler.institute)
