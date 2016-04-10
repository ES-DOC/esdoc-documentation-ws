# -*- coding: utf-8 -*-
"""
.. module:: docs.py
   :platform: Unix
   :synopsis: Data access operations across docs domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy as sa

from esdoc_api.db.dao.core import (
    delete_by_type,
    delete_by_id,
    delete_by_facet,
    sort
    )
from esdoc_api.db import models, session
from esdoc_api.db.models import (
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentSummary,
    Institute,
    Project
)



def get_document(uid, version, project_id=None):
    """Returns a Document instance by it's project, UID & version.

    :param int project_id: ID of a Project instance.
    :param str uid: Document unique identifier.
    :param str version: Document version.

    :returns: First matching document.
    :rtype: db.models.Document

    """
    qry = session.query(Document)

    if project_id is not None:
        qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(Document.uid == unicode(uid))
    if version is None or version in models.DOCUMENT_VERSIONS:
        qry = qry.order_by(Document.version.desc())
    else:
        qry = qry.filter(Document.version == int(version))

    return qry.all() if version == models.DOCUMENT_VERSION_ALL else qry.first()


def get_document_by_name(
    project_id,
    typeof,
    name,
    institute_id=None,
    latest_only=True
    ):
    """Retrieves a single document by it's name.

    :param int project_id: ID of a Project instance.
    :param str typeof: Document type.
    :param str name: Document name.
    :param int institute_id: ID of an Institute instance.
    :param boolean latest_only: Project with which document is associated.

    :returns: First matching document.
    :rtype: db.models.Document

    """
    qry = session.query(Document)

    qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(sa.func.upper(Document.type) == typeof.upper())
    qry = qry.filter(sa.func.upper(Document.name) == name.upper())
    if institute_id is not None:
        qry = qry.filter(Document.institute_id == institute_id)
    if latest_only == True:
        qry = qry.filter(Document.is_latest == True)

    return qry.first()


def get_document_by_type(project_id, typeof, latest_only=True):
    """Retrieves documents by type.

    :param int project_id: ID of a Project instance.
    :param str typeof: Document type.
    :param boolean latest_only: Flag indicating whether to return only the latest documents.

    :returns: Matching documents.
    :rtype: list

    """
    qry = session.query(Document)

    qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(sa.func.upper(Document.type) == typeof.upper())
    if latest_only == True:
        qry = qry.filter(Document.is_latest == True)

    return qry.all()


def get_document_by_drs_keys(
    project_id,
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

    :param int project_id: ID of a Project instance.
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

    qry = qry.filter(Document.project_id == project_id)
    if key_01 is not None:
        qry = qry.filter(DocumentDRS.key_01 == key_01.upper())
    if key_02 is not None:
        qry = qry.filter(DocumentDRS.key_02 == key_02.upper())
    if key_03 is not None:
        qry = qry.filter(DocumentDRS.key_03 == key_03.upper())
    if key_04 is not None:
        qry = qry.filter(DocumentDRS.key_04 == key_04.upper())
    if key_05 is not None:
        qry = qry.filter(DocumentDRS.key_05 == key_05.upper())
    if key_06 is not None:
        qry = qry.filter(DocumentDRS.key_06 == key_06.upper())
    if key_07 is not None:
        qry = qry.filter(DocumentDRS.key_07 == key_07.upper())
    if key_08 is not None:
        qry = qry.filter(DocumentDRS.key_08 == key_08.upper())
    if latest_only == True:
        qry = qry.filter(Document.is_latest == True)

    return qry.first()


def get_documents_by_external_id(project_id, external_id):
    """Retrieves a list of documents with a matching external ID.

    :param int project_id: ID of a Project instance.
    :param str external_id: External ID to be resolved to a document.

    :returns: List of Document instances with matching external ID.
    :rtype: list

    """
    qry = session.query(Document).join(DocumentExternalID)

    qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(DocumentExternalID.external_id.like('%' + external_id.upper() + '%'))

    return qry.all()


def get_document_drs(project_id, document_id, path):
    """Returns a DocumentDRS instance with matching document & drs path.

    :param int project_id: ID of a Project instance.
    :param int document_id: ID of a Document instance.
    :param str path: DRS path.

    :returns: First DocumentDRS instance with matching document & drs path.
    :rtype: db.models.DocumentDRS

    """
    qry = session.query(DocumentDRS)

    qry = qry.filter(DocumentDRS.project_id == project_id)
    qry = qry.filter(DocumentDRS.document_id == document_id)
    qry = qry.filter(DocumentDRS.path == path.upper())

    return qry.first()


def get_document_external_id(project_id, document_id, external_id):
    """Returns a DocumentExternalID instance with matching document & external id.

    :param int project_id: ID of a Project instance.
    :param int document_id: ID of a Document instance.
    :param str external_id: An external ID.

    :returns: First DocumentExternalID instance with matching document & external id.
    :rtype: db.models.DocumentExternalID

    """
    qry = session.query(DocumentExternalID)

    qry = qry.filter(DocumentExternalID.project_id == project_id)
    qry = qry.filter(DocumentExternalID.document_id == document_id)
    qry = qry.filter(DocumentExternalID.external_id == external_id)

    return qry.first()


def get_document_external_ids(document_id, project_id=None):
    """Returns a DocumentExternalID instance with matching document & external id.

    :param int document_id: ID of a Document instance.
    :param int project_id: ID of a Project instance.

    :returns: First DocumentExternalID instance with matching document & external id.
    :rtype: db.models.DocumentExternalID

    """
    qry = session.query(DocumentExternalID)

    qry = qry.filter(DocumentExternalID.document_id == document_id)
    if project_id is not None:
        qry = qry.filter(DocumentExternalID.project_id == project_id)

    return qry.all()


def get_document_summary(document_id, language_id):
    """Returns a DocumentSummary instance with matching document & language.

    :param int document_id: ID of a Document instance.
    :param int language_id: ID of a DocumentLanguage instance.

    :returns: First DocumentSummary instance with matching document & language.
    :rtype: db.models.DocumentSummary

    """
    qry = session.query(DocumentSummary)

    qry = qry.filter(DocumentSummary.document_id == document_id)
    qry = qry.filter(DocumentSummary.language_id == language_id)

    return qry.first()


def get_document_summaries(
    project_id,
    type,
    version,
    language_id,
    institute_id=None,
    model=None,
    experiment=None
    ):
    """Returns a list of DocumentSummary instance with matching criteria.

    :param int project_id: ID of a Project instance.
    :param str type: Document type.
    :param str version: Document version (latest | all).
    :param int language_id: ID of a DocumentLanguage instance.
    :param int institute_id: ID of an Institute instance.

    :returns: First DocumentSummary instance with matching document & language.
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
    qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(DocumentSummary.language_id == language_id)
    if type != models.DOCUMENT_TYPE_ALL:
        qry = qry.filter(sa.func.upper(Document.type) == type)
    if version == models.DOCUMENT_VERSION_LATEST:
        qry = qry.filter(Document.is_latest == True)
    if experiment is not None:
        qry = qry.filter(sa.func.upper(DocumentSummary.experiment) == experiment)
    if institute_id is not None:
        qry = qry.filter(Document.institute_id == institute_id)
    if model is not None:
        qry = qry.filter(sa.func.upper(DocumentSummary.model) == model)

    # Apply query limit.
    qry = qry.limit(session.QUERY_LIMIT)

    return sort(DocumentSummary, qry.all())


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


def delete_document(document_id):
    """Deletes a document.

    :param int document_id: ID of a Document instance.

    """
    delete_document_drs(document_id)
    delete_document_external_ids(document_id)
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
                        Document.project_id,
                        Document.type)

    qry = qry.group_by(Document.project_id)
    qry = qry.group_by(Document.type)

    return qry.all()


def get_document_counts():
    """Returns document counts.

    :returns: List of counts over document types.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.institute_id),
                        Project.name,
                        Institute.name,
                        Document.type)
    qry = qry.join(Project)
    qry = qry.join(Institute)

    qry = qry.group_by(Project.id)
    qry = qry.group_by(Institute.id)
    qry = qry.group_by(Document.type)

    qry = qry.order_by(Document.type.desc())

    return qry.all()


def get_document_type_count(project_id, typeof):
    """Returns count over a project's document type.

    :param str typeof: Document type.
    :param int project_id: ID of a Project instance.

    :returns: List of counts over a project's document types.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.type))

    qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(sa.func.upper(Document.type) == typeof.upper())
    qry = qry.group_by(Document.type)

    counts = qry.all()

    return 0 if not len(counts) else counts[0][0]


def get_doc_descriptions(project_id, language_id, typeof):
    """Returns document descriptions.

    :param int project_id: ID of a Project instance.
    :param int language_id: ID of a DocumentLanguage instance.
    :param str typeof: Type of Document instance.

    :returns: Dictionary of project document desciptions.
    :rtype: dict

    """
    qry = session.query(Document.name, DocumentSummary.description)
    qry = qry.join(DocumentSummary)

    qry = qry.filter(Document.is_latest == True)
    qry = qry.filter(Document.project_id == project_id)
    qry = qry.filter(Document.type == typeof)
    qry = qry.filter(DocumentSummary.language_id == language_id)

    return qry.all()


def _get_summary_fieldset(field):
    """Returns set of unique document summary field values.

    """
    qry = session.query(Document.project_id, field)
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
