# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_id.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by id search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db



# Query parameter names.
_PARAM_DOCUMENT_ID = 'id'
_PARAM_DOCUMENT_VERSION = 'version'

# Query parameter validation schema.
REQUEST_VALIDATION_SCHEMA = {
    _PARAM_DOCUMENT_ID: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_DOCUMENT_VERSION: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}


def decode_request(handler):
    """Decodes request parameters.

    """
    handler.id = handler.get_argument(_PARAM_DOCUMENT_ID)
    handler.version = handler.get_argument(_PARAM_DOCUMENT_VERSION)


def format_params(handler):
    """Formats request parameters.

    """
    handler.id = handler.id.lower()
    handler.version = handler.version.lower()


def do_search(handler):
    """Executes document search against db.

    :param handler: Request handler.

    :returns: Search result.
    :rtype: db.models.Document

    """
    yield db.dao.get_document(handler.id,
                              handler.version,
                              handler.project)
