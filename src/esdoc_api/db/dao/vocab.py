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
    Project
)



# Module exports.
__all__ = [
    'get_doc_language',
    'get_doc_ontology',
    'get_project_institute_counts',
    'create_project'
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
    name = unicode(name).lower()

    qry = session.query(DocumentOntology)

    qry = qry.filter(DocumentOntology.Name==name)

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
    code = unicode(code).lower()

    return get_by_facet(DocumentLanguage,
                        DocumentLanguage.Code==code)


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


def create_project(name, description, homepage):
    """Creates & returns a project instance.

    :param str name: Project name.
    :param str description: Project description.
    :param str homepage: Project home page.

    :returns: Newly created project instance.
    :rtype: db.models.Project

    """
    def _parse_param(param_val, param_name):
        """Parses an input parameter.

        """
        if param_val is None:
            raise ValueError(param_name)
        param_val = unicode(param_val).strip()
        if not param_val:
            raise ValueError(param_name)
        return param_val

    # Parse input params.
    name = _parse_param(name, 'name')
    description = _parse_param(description, 'description')
    homepage = _parse_param(homepage, 'homepage')

    # Instantiate new project.
    instance = Project()
    instance.Name =  name
    instance.Description =  description
    instance.URL =  homepage

    return instance
