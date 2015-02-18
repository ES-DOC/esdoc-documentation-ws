# -*- coding: utf-8 -*-
"""
.. module:: vocab.py
   :platform: Unix
   :synopsis: Data access operations across vocab domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy as sa

import pyesdoc

from esdoc_api.db import session
from esdoc_api.db.dao.core import get_by_facet
from esdoc_api.db.models import (
    Document,
    DocumentLanguage,
    DocumentOntology,
)



# Module exports.
__all__ = [
    'get_doc_language',
    'get_doc_ontology',
    'get_project_institute_counts'
]



def get_doc_ontology(name, version=None):
    """Returns a DocumentOntology instance with matching name & version.

    :param name: Ontology name.
    :type name: str

    :param version: Ontology version.
    :type version: str

    :returns: First DocumentOntology instance with matching name & version.
    :rtype: db.models.DocumentOntology

    """
    if version is not None:
        name += '.'
        name += str(version)

    qry = session.query(DocumentOntology)

    qry = qry.filter(DocumentOntology.Name==name.lower())

    return qry.first()


def get_doc_language(code=None):
    """Returns a DocumentLanguage instance by it's code.

    :param type: A supported entity type.
    :type type: class

    :param name: Entity code.
    :type name: str

    :returns: First DocumentLanguage with matching code.
    :rtype: db.models.DocumentLanguage

    """
    if code is None:
        code = pyesdoc.ESDOC_DEFAULT_LANGUAGE

    return get_by_facet(DocumentLanguage,
                        DocumentLanguage.Code==code.lower())


def get_project_institute_counts():
    """Returns institute counts grouped by project.

    :returns: List of counts over a project's institutes.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.Institute_ID),
                        Document.Project_ID,
                        Document.Institute_ID)

    qry = qry.group_by(Document.Project_ID)
    qry = qry.group_by(Document.Institute_ID)

    return qry.all()
