"""
.. module:: esdoc_api.models.search.document.py
   :copyright: Copyright "Apr 3, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates set of data access operations over a Document entity.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.models.entities.document import Document
from esdoc_api.models.entities.document_by_drs import DocumentByDRS
from esdoc_api.models.entities.document_by_external_id import DocumentByExternalID
from esdoc_api.models.entities.document_sub_document import DocumentSubDocument
from esdoc_api.models.entities.ingest_endpoint import IngestEndpoint
from esdoc_api.models.entities.institute import Institute
from esdoc_api.models.entities.project import Project


def set_is_latest(document, project):
    """Sets flag indicating whether this document is the latest version or not.

    :param document: A document for which the IsLatest flag is to be updated.
    :type document: esdoc_api.models.entities.document.Document

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    """
    # Defensive programming.
    if isinstance(document, Document) == False:
        raise TypeError('document')
    if isinstance(project, Project) == False:
        raise TypeError('project')

    # Retrieve latest.
    latest = Document.retrieve_by_id(project, document.UID)

    # Update flags when necessary.
    if latest is None or document.Version >= latest.Version:
        document.IsLatest = True
        if latest is not None and latest.ID != document.ID:
            latest.IsLatest = False


def retrieve(project, as_obj):
    """Retrieves a single document.

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    :param as_obj: Object representation of document.
    :type as_obj: object

    :returns: A document.
    :rtype: esdoc_api.models.entities.document.Document

    """
    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')
    if as_obj is None:
        raise ValueError('as_obj')

    # Retrieve.
    instance = Document.retrieve_by_id(project,
                                       as_obj.cim_info.id,
                                       as_obj.cim_info.version)

    # Assign.
    if instance is not None:
        instance.pycim_doc = as_obj

    return instance


def retrieve_children(parent):
    """Retrieves child documents.

    :param parent: A document for which the child documents are to be returned.
    :type parent: esdoc_api.models.entities.document.Document

    :returns: A collection of documents.
    :rtype: list

    """
    # Defensive programming.
    if isinstance(parent, Document) == False:
        raise TypeError('parent')

    return [i.Child for i in DocumentSubDocument.retrieve(parent)]


def retrieve_by_id(project, uid, version=None):
    """Retrieves a single document.

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    :param uid: Unique document identifier.
    :type uid: UUID

    :param version: Document version.
    :type version: str

    :returns: A document.
    :rtype: esdoc_api.models.entities.document.Document

    """
    from esdoc_api.models.entities.project import Project

    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')
    if uid is None:
        raise ValueError('document uid must be a universal identifier')

    # Set query.
    q = Document.query
    q = q.filter(Document.Project_ID==project.ID)
    q = q.filter(Document.UID==str(uid))
    if version is None:
        q = q.order_by(Document.Version.desc())
    else:
        q = q.filter(Document.Version==int(version))

    # Return first.
    return q.first()


def retrieve_by_name(project, type, name, institute=None, latest_only=True):
    """Retrieves a single document by it's name.

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    :param type: Document type.
    :type type: str

    :param name: Document name.
    :type name: str

    :param institute: The institute with which the document is associated.
    :type institute: esdoc_api.models.entities.institute.Institute

    :param latest_only: Flag indicating whether only the latest document is to be retrieved.
    :type latest_only: bool

    :returns: A document.
    :rtype: esdoc_api.models.entities.document.Document

    """
    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')
    if type is None:
        raise ValueError('type')
    if name is None:
        raise ValueError('name')
    if institute is not None and isinstance(institute, Institute) == False:
        raise TypeError('institute')

    # Set query.
    q = Document.query
    q = q.filter(Document.Project_ID==project.ID)
    q = q.filter(Document.Type==type.upper())
    q = q.filter(Document.Name==name.upper())
    if institute is not None:
        q = q.filter(Document.Institute_ID==institute.ID)
    if latest_only == True:
        q = q.filter(Document.IsLatest==True)

    # Return first.
    return q.first()


def retrieve_by_drs_keys(project,
                         key_01=None,
                         key_02=None,
                         key_03=None,
                         key_04=None,
                         key_05=None,
                         key_06=None,
                         key_07=None,
                         key_08=None,
                         latest_only = True):
    """Retrieves a single document set from matched drs keys.

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    :param key_01: DRS key 1.
    :type key_01: str

    :param key_02: DRS key 2.
    :type key_02: str

    :param key_03: DRS key 3.
    :type key_03: str

    :param key_04: DRS key 4.
    :type key_04: str

    :param key_05: DRS key 5.
    :type key_05: str

    :param key_06: DRS key 6.
    :type key_06: str

    :param key_07: DRS key 7.
    :type key_07: str

    :param key_08: DRS key 8.
    :type key_08: str

    :param latest_only: Flag indicating whether only the latest document is to be retrieved.
    :type latest_only: bool

    :returns: A document.
    :rtype: esdoc_api.models.entities.document.Document

    """
    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')

    # Get document via querying drs index table.
    instance = DocumentByDRS.retrieve_by_keys(project,
                                              key_01,
                                              key_02,
                                              key_03,
                                              key_04,
                                              key_05,
                                              key_06,
                                              key_07,
                                              key_08,
                                              latest_only)

    return None if instance is None else instance.Document


def retrieve_by_external_id(project, external_id):
    """Retrieves a document by searching by external id.

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    :param external_id: Document external identifier.
    :type external_id: str
    
    :returns: Collection of matching documents.
    :rtype: list

    """
    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')
    if external_id is None:
        raise ValueError('external_id')

    # Get document via querying external identifier index table.
    return [i.Document for i in DocumentByExternalID.retrieve(project,
                                                              external_id)]


def create(project, endpoint, as_obj):
    """Factory method to create and return an instance.

    :param project: The project with which the document is associated.
    :type project: esdoc_api.models.entities.project.Project

    :param endpoint: Endpoint with which document is associated.
    :type endpoint: esdoc_api.models.entities.endpoint.Endpoint

    :param as_obj: Object representation of document.
    :type as_obj: object

    """
    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')
    if isinstance(endpoint, IngestEndpoint) == False:
        raise TypeError('endpoint')
    if as_obj is None:
        raise ValueError('as_obj')

    # Instantiate & assign attributes.
    instance = Document()
    instance.pycim_doc = as_obj
    instance.Project_ID = project.ID
    instance.IngestEndpoint_ID = endpoint.ID
    instance.UID = str(as_obj.cim_info.id)
    instance.Version = int(as_obj.cim_info.version)
    instance.Type = as_obj.cim_info.type_info.type.upper()
    instance.Name = Document.get_name(instance)
    Document.set_is_latest(instance, project)

    return instance
