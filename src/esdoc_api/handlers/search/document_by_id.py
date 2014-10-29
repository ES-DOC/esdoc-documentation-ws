# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_id.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by id search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db



def get_url_params():
    """Returns url parameter specification."""
    return {
        'id': {
            'required': True,
            'value_formatter': lambda v : v.lower()
        },
        'version': {
            'required' : True,
            'value_formatter': lambda v : v.lower()
        }
    }


def do_search(criteria):
    """Executes document search against db.

    :param object: Search criteria.

    :returns: Search result.
    :rtype: db.models.Document | None

    """
    yield db.dao.get_document(criteria.project.ID,
                              criteria.id,
                              criteria.version)
