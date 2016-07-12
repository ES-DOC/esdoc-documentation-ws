# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_external_id.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by external ID search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import utils



# Query parameter names.
_PARAM_EXTERNAL_ID = 'externalID'
_PARAM_EXTERNAL_TYPE = 'externalType'

# Query parameter validation schema.
REQUEST_VALIDATION_SCHEMA = {
    _PARAM_EXTERNAL_ID: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_EXTERNAL_TYPE: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}


def decode_request(handler):
    """Decodes request parameters.

    """
    handler.external_id = handler.get_argument(_PARAM_EXTERNAL_ID)
    handler.external_type = handler.get_argument(_PARAM_EXTERNAL_TYPE)


def validate_params(handler):
    """Validates url request params.

    :param handler: Request handler.

    """
    # Validate that an external id handler exists.
    handler = utils.external_id.get(handler.project, handler.external_type)
    if not handler:
        raise ValueError("External ID type is unsupported.")

    # Validate external id.
    if not handler.is_valid(handler.external_id):
        raise ValueError("Request parameter externalID: is invalid.")


def do_search(handler):
    """Executes document search against db.

    :param handler: Request handler.

    :returns: Search result.
    :rtype: db.models.Document

    """
    # Set search manager.
    manager = utils.external_id.get(handler.project, handler.external_type)

    # Set parsed external id.
    external_id = manager.get_parsed(handler.external_id)

    # Yield search results.
    for doc in manager.do_search(handler.project, external_id):
        yield doc
