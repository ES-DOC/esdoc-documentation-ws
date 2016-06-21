# -*- coding: utf-8 -*-
"""
.. module:: docs.py
   :platform: Unix
   :synopsis: Data access operations across docs domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy as sa

import pyesdoc

from esdoc_api.db import session
from esdoc_api.db.dao.core import text_filter
from esdoc_api.db.models import Document
from esdoc_api.db.models import DocumentSubProject



def get_project_institute_counts():
    """Returns institute counts grouped by project.

    :returns: List of counts over a project's institutes.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.institute),
                        Document.project,
                        Document.institute)
    qry = qry.group_by(Document.project)
    qry = qry.group_by(Document.institute)

    return qry.all()


def get_project_document_type_counts():
    """Returns document type counts grouped by project.

    :returns: List of counts over a project's document types.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.type),
                        Document.project,
                        Document.type)
    qry = qry.group_by(Document.project)
    qry = qry.group_by(Document.type)

    return qry.all()


def get_document_type_count(project, typeof):
    """Returns count over a project's document type.

    :param str typeof: Document type.
    :param str project: Project code.

    :returns: List of counts over a project's document types.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.type))
    qry = text_filter(qry, Document.project, project)
    qry = text_filter(qry, Document.type, typeof)
    qry = qry.group_by(Document.type)

    counts = qry.all()

    return 0 if not len(counts) else counts[0][0]


def get_document_types():
    """Returns list of indexed document types.

    :returns: List of indexed document types.
    :rtype: list

    """
    qry = session.query(
        Document.project,
        Document.type
        )
    qry = qry.filter(Document.type != 'None')
    qry = qry.filter(Document.type is not None)
    qry = qry.distinct()

    return qry.all()


def get_experiments():
    """Returns list of indexed experiments.

    :returns: List of indexed experiments.
    :rtype: list

    """
    qry = session.query(
        Document.project,
        Document.experiment
        )
    qry = qry.filter(Document.experiment != 'None')
    qry = qry.filter(Document.experiment is not None)
    qry = qry.distinct()

    return qry.all()


def get_institutes():
    """Returns list of indexed institutes.

    :returns: List of indexed institutes.
    :rtype: list

    """
    qry = session.query(
        Document.project,
        Document.institute
        )
    qry = qry.filter(Document.institute != 'None')
    qry = qry.filter(Document.institute is not None)
    qry = qry.distinct()

    return qry.all()


def get_models():
    """Returns list of indexed models.

    :returns: List of indexed models.
    :rtype: list

    """
    qry = session.query(
        Document.project,
        Document.model
        )
    qry = qry.filter(Document.model != 'None')
    qry = qry.filter(Document.model is not None)
    qry = qry.distinct()

    return qry.all()


def get_projects():
    """Returns list of indexed projects.

    :returns: List of indexed projects.
    :rtype: list

    """
    qry = session.query(Document.project)
    qry = qry.filter(Document.project != 'None')
    qry = qry.filter(Document.project is not None)
    qry = qry.distinct()

    return sorted([i[0] for i in qry.all() if i[0]])


def get_sub_projects():
    """Returns list of indexed sub-projects.

    :returns: List of indexed sub-projects.
    :rtype: list

    """
    qry = session.query(
        DocumentSubProject.project,
        DocumentSubProject.sub_project
        )
    qry = qry.distinct()

    return qry.all()
