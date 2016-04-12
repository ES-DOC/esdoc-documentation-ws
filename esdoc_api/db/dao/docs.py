# -*- coding: utf-8 -*-
"""
.. module:: docs.py
   :platform: Unix
   :synopsis: Data access operations across docs domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy as sa

import pyesdoc

from esdoc_api.db.dao.core import delete_by_type
from esdoc_api.db.dao.core import delete_by_id
from esdoc_api.db.dao.core import delete_by_facet
from esdoc_api.db.dao.core import text_filter
from esdoc_api.db.dao.core import sort
from esdoc_api.db import models, session
from esdoc_api.db.models import Document
from esdoc_api.db.models import DocumentDRS
from esdoc_api.db.models import DocumentExternalID
from esdoc_api.db.models import DocumentSubProject
from esdoc_api.db.models import DocumentSummary
from esdoc_api.db.models import Institute



def get_document(uid, version, project=None):
    """Returns a Document instance by it's project, UID & version.

    :param str uid: Document unique identifier.
    :param str version: Document version.
    :param str project: Project code.

    :returns: First matching document.
    :rtype: db.models.Document

    """
    qry = session.query(Document)
    if project:
        qry = text_filter(qry, Document.project, project)
    qry = qry.filter(Document.uid == unicode(uid))
    if version is None or version in models.DOCUMENT_VERSIONS:
        qry = qry.order_by(Document.version.desc())
    else:
        qry = qry.filter(Document.version == int(version))

    return qry.all() if version == models.DOCUMENT_VERSION_ALL else qry.first()


def get_document_by_name(
    project,
    typeof,
    name,
    institute=None,
    latest_only=True
    ):
    """Retrieves a single document by it's name.

    :param str project: Project code.
    :param str typeof: Document type.
    :param str name: Document name.
    :param str institute: Institute code.
    :param boolean latest_only: Project with which document is associated.

    :returns: First matching document.
    :rtype: db.models.Document

    """
    qry = session.query(Document)
    qry = text_filter(qry, Document.project, project)
    qry = text_filter(qry, Document.type, typeof)
    qry = text_filter(qry, Document.name, name)
    if institute:
        qry = text_filter(qry, Document.institute, institute)
    if latest_only == True:
        qry = qry.filter(Document.is_latest == True)

    return qry.first()


def get_document_by_type(project, typeof, latest_only=True):
    """Retrieves documents by type.

    :param str project: Project code.
    :param str typeof: Document type.
    :param boolean latest_only: Flag indicating whether to return only the latest documents.

    :returns: Matching documents.
    :rtype: list

    """
    qry = session.query(Document)
    qry = text_filter(qry, Document.project, project)
    qry = text_filter(qry, Document.type, typeof)
    if latest_only == True:
        qry = qry.filter(Document.is_latest == True)

    return qry.all()


def get_document_by_drs_keys(
    project,
    key_01=None,
    key_02=None,
    key_03=None,
    key_04=None,
    key_05=None,
    key_06=None,
    key_07=None,
    key_08=None,
    latest_only = True
    ):
    """Retrieves a single document by it's drs keys.

    :param str project: Project code.
    :param str key_01: DRS key 1.
    :param str key_02: DRS key 2.
    :param str key_03: DRS key 3.
    :param str key_04: DRS key 4.
    :param str key_05: DRS key 5.
    :param str key_06: DRS key 6.
    :param str key_07: DRS key 7.
    :param str key_08: DRS key 8.
    :param boolean latest_only: Flag indicating whether only the latest document is to be returned.

    :returns: First matching document.
    :rtype: db.models.Document

    """
    qry = session.query(Document).join(DocumentDRS)
    qry = text_filter(qry, Document.project, project)
    if key_01:
        qry = text_filter(qry, DocumentDRS.key_01, key_01)
    if key_02:
        qry = text_filter(qry, DocumentDRS.key_02, key_02)
    if key_03:
        qry = text_filter(qry, DocumentDRS.key_03, key_03)
    if key_04:
        qry = text_filter(qry, DocumentDRS.key_04, key_04)
    if key_05:
        qry = text_filter(qry, DocumentDRS.key_05, key_05)
    if key_06:
        qry = text_filter(qry, DocumentDRS.key_06, key_06)
    if key_07:
        qry = text_filter(qry, DocumentDRS.key_07, key_07)
    if key_08:
        qry = text_filter(qry, DocumentDRS.key_08, key_08)
    if latest_only == True:
        qry = qry.filter(Document.is_latest == True)

    return qry.first()


def get_documents_by_external_id(project, external_id):
    """Retrieves a list of documents with a matching external ID.

    :param str project: Project code.
    :param str external_id: External ID to be resolved to a document.

    :returns: List of Document instances with matching external ID.
    :rtype: list

    """
    qry = session.query(Document).join(DocumentExternalID)
    qry = text_filter(qry, Document.project, project)
    qry = qry.filter(DocumentExternalID.external_id.like('%' + external_id.upper() + '%'))

    return qry.all()


def get_document_summaries(
    project,
    type,
    version,
    institute=None,
    model=None,
    experiment=None
    ):
    """Returns a list of DocumentSummary instance with matching criteria.

    :param str project: Project code.
    :param str type: Document type.
    :param str version: Document version (latest | all).
    :param str institute: Institute code.

    :returns: First DocumentSummary instance with matching document.
    :rtype: db.models.DocumentSummary

    """
    # Format params.
    version = version.lower()
    type = type.upper()
    if model:
        model = model.upper()
    if experiment:
        experiment = experiment.upper()

    # Set query.
    qry = session.query(DocumentSummary).join(Document)

    # Set mandatory params.
    qry = text_filter(qry, Document.project, project)
    if type != models.DOCUMENT_TYPE_ALL:
        qry = text_filter(qry, Document.type, type)
    if version == models.DOCUMENT_VERSION_LATEST:
        qry = qry.filter(Document.is_latest == True)
    if experiment:
        qry = text_filter(qry, DocumentSummary.experiment, experiment)
    if institute:
        qry = text_filter(qry, Document.institute, institute)
    if model:
        qry = text_filter(qry, DocumentSummary.model, model)

    # Apply query limit.
    qry = qry.limit(session.QUERY_LIMIT)

    return sort(DocumentSummary, qry.all())


def get_document_projects():
    """Returns set of distinct document project associations.

    """
    qry = session.query(
        DocumentSubProject.project,
        DocumentSubProject.sub_project
        )
    qry = qry.distinct()

    return qry.all()


def _delete_document_relation(document_id, typeof):
    """Deletes all document relations of passed type.

    :param int document_id: ID of a Document instance.
    :param class typeof: Type of relation.

    """
    delete_by_facet(typeof, typeof.document_id == document_id)


def delete_document_summaries(document_id):
    """Deletes a list of DocumentSummary instances filtered by their Document ID.

    :param int document_id: ID of a Document instance.

    """
    _delete_document_relation(document_id, DocumentSummary)


def delete_document_external_ids(document_id):
    """Deletes a list of DocumentExternalID instances filtered by their Document ID.

    :param int document_id: ID of a Document instance.

    """
    _delete_document_relation(document_id, DocumentExternalID)


def delete_document_drs(document_id):
    """Deletes a list of DocumentDRS instances filtered by their Document ID.

    :param int document_id: ID of a Document instance.

    """
    _delete_document_relation(document_id, DocumentDRS)


def delete_document_sub_project(document_id):
    """Deletes a list of DocumentSubProject instances filtered by their Document ID.

    :param int document_id: ID of a Document instance.

    """
    _delete_document_relation(document_id, DocumentSubProject)


def delete_document(document_id):
    """Deletes a document.

    :param int document_id: ID of a Document instance.

    """
    delete_document_drs(document_id)
    delete_document_external_ids(document_id)
    delete_document_sub_project(document_id)
    delete_document_summaries(document_id)
    delete_by_id(Document, document_id)


def delete_all_documents():
    """Deletes all documents.

    """
    delete_by_type(Document, delete_document)


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


def get_document_counts():
    """Returns document counts.

    :returns: List of counts over document types.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.institute),
                        Document.project,
                        Institute.name,
                        Document.type)
    qry = qry.join(Institute)
    qry = qry.group_by(Document.project)
    qry = qry.group_by(Institute.id)
    qry = qry.group_by(Document.type)
    qry = qry.order_by(Document.type.desc())

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


def _get_summary_fieldset(field):
    """Returns set of unique document summary field values.

    """
    qry = session.query(Document.project, field)
    qry = qry.join(DocumentSummary)
    qry = qry.filter(field != 'None')
    qry = qry.distinct()

    return qry.all()


def get_summary_model_set():
    """Returns set of unique document summary model names.

    """
    return _get_summary_fieldset(DocumentSummary.model)


def get_summary_eperiment_set():
    """Returns set of unique document summary experiment names.

    """
    return _get_summary_fieldset(DocumentSummary.experiment)
