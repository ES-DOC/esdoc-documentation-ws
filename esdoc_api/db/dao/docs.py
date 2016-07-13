# -*- coding: utf-8 -*-
"""
.. module:: docs.py
   :platform: Unix
   :synopsis: Data access operations across docs domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api import constants
from esdoc_api.db import session
from esdoc_api.db.dao.core import delete_by_id
from esdoc_api.db.dao.core import delete_by_facet
from esdoc_api.db.dao.core import like_filter
from esdoc_api.db.dao.core import text_filter
from esdoc_api.db.dao.core import sort
from esdoc_api.db.models import Document
from esdoc_api.db.models import DocumentDRS
from esdoc_api.db.models import DocumentExternalID
from esdoc_api.db.models import DocumentSubProject



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
    if version is None or version in constants.DOCUMENT_VERSIONS:
        qry = qry.order_by(Document.version.desc())
    else:
        qry = qry.filter(Document.version == int(version))

    return qry.all() if version == constants.DOCUMENT_VERSION_ALL else qry.first()


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
    qry = like_filter(qry, DocumentExternalID.external_id, external_id.upper())

    return qry.all()


def get_document_summaries(
    project,
    typeof,
    version,
    sub_project=None,
    institute=None,
    model=None,
    experiment=None
    ):
    """Returns document summary information.

    :param str project: Project code.
    :param str typeof: Document type.
    :param str version: Document version (latest | all).
    :param str sub_project: Sub-project code.
    :param str institute: Institute code.
    :param str model: Model code.
    :param str experiment: Experiment code.

    :returns: List of matching documents.
    :rtype: db.models.Document

    """
    # Format params.
    version = version.lower()
    typeof = typeof.upper()
    if model:
        model = model.upper()
    if experiment:
        experiment = experiment.upper()

    # Set query.
    qry = session.query(
        Document.description,
        Document.experiment,
        Document.field_01,
        Document.field_02,
        Document.field_03,
        Document.field_04,
        Document.field_05,
        Document.field_06,
        Document.field_07,
        Document.field_08,
        Document.id,
        Document.ingest_date,
        Document.institute,
        Document.is_latest,
        Document.language,
        Document.long_name,
        Document.model,
        Document.name,
        Document.project,
        Document.short_name,
        Document.source,
        Document.type,
        Document.uid,
        Document.version,
        Document.sub_projects,
        Document.alternative_name
        )

    # Set mandatory params.
    qry = text_filter(qry, Document.project, project)
    qry = qry.filter(Document.short_name != u"")

    if typeof != constants.DOCUMENT_TYPE_ALL:
        qry = text_filter(qry, Document.type, typeof)
    if version == constants.DOCUMENT_VERSION_LATEST:
        qry = qry.filter(Document.is_latest == True)
    if experiment:
        qry = text_filter(qry, Document.experiment, experiment)
    if institute:
        qry = text_filter(qry, Document.institute, institute)
    if model:
        qry = text_filter(qry, Document.model, model)
    if sub_project:
        qry = like_filter(qry, Document.sub_projects, "<{}>".format(sub_project.lower()))

    # Apply query limit.
    try:
        load_all = constants.MAPPED_DOCUMENT_TYPES[typeof]['loadAll']
    except AttributeError:
        load_all = False
    if not load_all:
        qry = qry.limit(session.QUERY_LIMIT)

    return sort(Document, qry.all())


def _delete_document_relation(document_id, typeof):
    """Deletes all document relations of passed type.

    :param int document_id: ID of a Document instance.
    :param class typeof: Type of relation.

    """
    delete_by_facet(typeof, typeof.document_id == document_id)


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
    delete_by_id(Document, document_id)
