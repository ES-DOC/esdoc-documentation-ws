# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_name.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document by name search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db



def get_url_params():
    """Returns url parameter specification.

    """
    return {
        'institute': {
            'required' : False,
            'value_formatter' : lambda k: k.lower()
        },
        'name': {
            'required' : True,
        },
        'type': {
            'required' : True,
        }
    }


def do_search(criteria):
    """Executes document search against db.

    :param object: Search criteria.

    :returns: Search result.
    :rtype: db.models.Document | None

    """
    yield db.dao.get_document_by_name(criteria.project,
                                      criteria.type,
                                      criteria.name,
                                      criteria.institute)
