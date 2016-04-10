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
from esdoc_api.db.models import Document
from esdoc_api.db.models import DocumentLanguage
from esdoc_api.db.models import DocumentOntology
from esdoc_api.db.models import Institute
from esdoc_api.db.models import Project



def _parse_param(param_val, param_name):
    """Parses an input parameter.

    """
    if param_val is None:
        raise ValueError(param_name)
    param_val = unicode(param_val).strip()
    if not param_val:
        raise ValueError(param_name)
    return param_val


def get_doc_ontology(name, version=None):
    """Returns a DocumentOntology instance with matching name & version.

    :param str name: Ontology name.
    :param str version: Ontology version.

    :returns: First DocumentOntology instance with matching name & version.
    :rtype: db.models.DocumentOntology

    """
    if version is not None:
        name += '.'
        name += str(version)
    name = unicode(name).lower()

    qry = session.query(DocumentOntology)

    qry = qry.filter(DocumentOntology.name == name)

    return qry.first()


def get_doc_language(code=None):
    """Returns a DocumentLanguage instance by it's code.

    :param str code: Language code.

    :returns: First DocumentLanguage with matching code.
    :rtype: db.models.DocumentLanguage

    """
    if code is None:
        code = pyesdoc.DEFAULT_LANGUAGE
    code = unicode(code).lower()

    return get_by_facet(DocumentLanguage,
                        DocumentLanguage.code == code)


def get_project_institute_counts():
    """Returns institute counts grouped by project.

    :returns: List of counts over a project's institutes.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.institute_id),
                        Document.project_id,
                        Document.institute_id)

    qry = qry.group_by(Document.project_id)
    qry = qry.group_by(Document.institute_id)

    return qry.all()


def create_institute(name, long_name=None, country_code=None, homepage=None):
    """Creates & returns an institute instance.

    :param str name: Institute name.
    :param str long_name: Institute long name.
    :param str country_code: Institute country code.
    :param str homepage: Institute home page.

    :returns: Newly created institute instance.
    :rtype: db.models.Institute

    """
    name = name.upper()
    if not long_name:
        long_name = name
    if not country_code:
        country_code = "--"

    instance = Institute()
    instance.country_code = _parse_param(country_code, 'country_code')
    instance.long_name = _parse_param(long_name, 'long_name')
    instance.name = _parse_param(name, 'name')
    if homepage:
        instance.url = _parse_param(homepage, 'homepage')

    return instance


def create_project(name, description=None, homepage=None):
    """Creates & returns a project instance.

    :param str name: Project name.
    :param str description: Project description.
    :param str homepage: Project home page.

    :returns: Newly created project instance.
    :rtype: db.models.Project

    """
    name = name.upper()
    if not description:
        description = name

    instance = Project()
    instance.name = _parse_param(name, 'name')
    instance.description = _parse_param(description, 'description')
    if homepage:
        instance.url = _parse_param(homepage, 'homepage')

    return instance
