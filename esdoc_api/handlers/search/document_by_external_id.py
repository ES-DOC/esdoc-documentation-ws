# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_external_id.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by external ID search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import utils



def get_url_params():
    """Returns url parameter specification."""
    return {
        'externalID': {
            'required' : True,
        },
        'externalType': {
            'required' : True,
        }
    }


def parse_url_params(params):
    """Parses url request params.

    :param object: Search criteria.

    """
    # Validate that an external id handler exists.
    handler = utils.external_id.get(params.project, params.external_type)
    if not handler:
        raise ValueError("External ID type is unsupported.")

    # Validate external id.
    if not handler.is_valid(params.external_id):
        raise ValueError("Request parameter externalID: is invalid.")


def do_search(criteria):
    """Executes document search against db.

    :param object: Search criteria.

    :returns: Search result.
    :rtype: db.models.Document | None

    """
    handler = utils.external_id.get(criteria.project, criteria.external_type)
    external_id = handler.get_parsed(criteria.external_id)
    for doc in handler.do_search(criteria.project, external_id):
        yield doc
