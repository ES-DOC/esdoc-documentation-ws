"""
.. module:: esdoc_api.lib.repo.dao.custom.py
   :platform: Unix
   :synopsis: Set of custom repo data access operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import sqlalchemy as sa

from esdoc_api.lib.repo.dao_core import (
    delete_by_type,
    delete_by_id,
    delete_by_facet,
    get_by_id,
    get_by_facet,
    get_by_name,
    sort
    )
from esdoc_api.models import (
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentLanguage,
    DocumentOntology,
    DocumentRepresentation,
    DocumentSubDocument,
    DocumentSummary,
    Facet,
    FacetType,
    FacetRelation,
    FacetRelationType,
    IngestEndpoint,
    IngestURL
)
import esdoc_api.models as models
import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.repo.session as session



# Module exports.
__all__ = [
    'delete_all_documents',
    'delete_document',
    'delete_document_drs',
    'delete_document_external_ids',
    'delete_document_representations',
    'delete_document_sub_documents',
    'delete_document_summaries',
    'get_document',
    'get_document_by_drs_keys',
    'get_document_by_name',
    'get_doc_descriptions',
    'get_document_drs',
    'get_document_external_id',
    'get_document_external_ids',
    'get_doc_language',
    'get_doc_ontology',
    'get_doc_representation',
    'get_document_sub_document',
    'get_document_sub_documents',
    'get_document_summaries',
    'get_document_summary',
    'get_documents_by_external_id',
    'get_facet',
    'get_facet_relation',
    'get_facet_relation_types',
    'get_facet_types',
    'get_ingest_endpoints',
    'get_ingest_endpoint',
    'get_ingest_url',
    'get_project_document_language_counts',
    'get_project_document_type_counts'
]



def get_document(project_id, uid, version=models.DOCUMENT_VERSION_LATEST):
    """Returns a Document instance by it's project, UID & version.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param uid: Document unique identifier.
    :type uid: str

    :param version: Document version.
    :type version: str

    :returns: First matching document.
    :rtype: esdoc_api.models.Document

    """

    q = session.query(Document)
    if project_id is not None:
        q = q.filter(Document.Project_ID==project_id)
    q = q.filter(Document.UID==unicode(uid))
    if version is None or version in models.DOCUMENT_VERSIONS:
        q = q.order_by(Document.Version.desc())
    else:
        q = q.filter(Document.Version==int(version))

    return q.all() if version == models.DOCUMENT_VERSION_ALL else q.first()
    

def get_document_by_name(project_id, 
                         type,
                         name,
                         institute_id=None,
                         latest_only=True):
    """Retrieves a single document by it's name.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param type: Document type.
    :type type: str

    :param name: Document name.
    :type name: str

    :param institute_id: ID of an Institute instance.
    :type institute_id: int

    :param latest_only: Project with which document is associated.
    :type latest_only: boolean

    :returns: First matching document.
    :rtype: esdoc_api.models.Document

    """
    q = session.query(Document)
    q = q.filter(Document.Project_ID==project_id)
    q = q.filter(sa.func.upper(Document.Type)==type.upper())
    q = q.filter(sa.func.upper(Document.Name)==name.upper())    
    if institute_id is not None:
        q = q.filter(Document.Institute_ID==institute_id)
    if latest_only == True:
        q = q.filter(Document.IsLatest==True)

    return q.first()


def get_document_by_drs_keys(project_id,
                             key_01=None,
                             key_02=None,
                             key_03=None,
                             key_04=None,
                             key_05=None,
                             key_06=None,
                             key_07=None,
                             key_08=None,
                             latest_only = True):
    """Retrieves a single document by it's drs keys.

    :param project_id: ID of a Project instance.
    :type project_id: int

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

    :param latest_only: Flag indicating whether only the latest document is to be returned.
    :type latest_only: boolean

    :returns: First matching document.
    :rtype: esdoc_api.models.Document

    """
    q = session.query(Document).join(DocumentDRS)
    q = q.filter(Document.Project_ID==project_id)
    if key_01 is not None:
        q = q.filter(DocumentDRS.Key_01==key_01.upper())
    if key_02 is not None:
        q = q.filter(DocumentDRS.Key_02==key_02.upper())
    if key_03 is not None:
        q = q.filter(DocumentDRS.Key_03==key_03.upper())
    if key_04 is not None:
        q = q.filter(DocumentDRS.Key_04==key_04.upper())
    if key_05 is not None:
        q = q.filter(DocumentDRS.Key_05==key_05.upper())
    if key_06 is not None:
        q = q.filter(DocumentDRS.Key_06==key_06.upper())
    if key_07 is not None:
        q = q.filter(DocumentDRS.Key_07==key_07.upper())
    if key_08 is not None:
        q = q.filter(DocumentDRS.Key_08==key_08.upper())
    if latest_only == True:
        q = q.filter(Document.IsLatest==True)

    return q.first()


def get_documents_by_external_id(project_id, external_id):
    """Retrieves a list of documents with a matching external ID.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param external_id: External ID to be resolved to a document.
    :type external_id: str

    :returns: List of Document instances with matching external ID.
    :rtype: list

    """
    q = session.query(Document).join(DocumentExternalID)
    q = q.filter(Document.Project_ID==project_id)
    q = q.filter(DocumentExternalID.ExternalID.like('%' + external_id.upper() + '%'))

    return q.all()


def get_document_sub_document(parent_id, child_id):
    """Retrieves a list of document child documents.

    :param parent_id: ID of parent Document instance.
    :type parent_id: int

    :param parent_id: ID of parent Document instance.
    :type parent_id: int

    :returns: A DocumentSubDocument instance.
    :rtype: DocumentSubDocument or None

    """
    q = session.query(DocumentSubDocument)
    q = q.filter(DocumentSubDocument.Document_ID==parent_id)
    q = q.filter(DocumentSubDocument.SubDocument_ID==child_id)

    return q.first()


def get_document_sub_documents(document_id):
    """Retrieves a list of document child documents.

    :param document_id: ID of a Document instance.
    :type document_id: int

    :returns: List of child Document instances.
    :rtype: list

    """
    q = session.query(DocumentSubDocument)
    q = q.filter(DocumentSubDocument.Document_ID==document_id)

    return map(lambda sd: get_by_id(Document, sd.SubDocument_ID), q.all())


def get_document_drs(project_id, document_id, path):
    """Returns a DocumentDRS instance with matching document & drs path.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param document_id: ID of a Document instance.
    :type document_id: int

    :param path: DRS path.
    :type path: str

    :returns: First DocumentDRS instance with matching document & drs path.
    :rtype: esdoc_api.models.DocumentDRS

    """
    q = session.query(DocumentDRS)
    q = q.filter(DocumentDRS.Project_ID==project_id)
    q = q.filter(DocumentDRS.Document_ID==document_id)
    q = q.filter(DocumentDRS.Path==path.upper())

    return q.first()


def get_document_external_id(project_id, document_id, external_id):
    """Returns a DocumentExternalID instance with matching document & external id.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param document_id: ID of a Document instance.
    :type document_id: int

    :param external_id: An external ID.
    :type external_id: str

    :returns: First DocumentExternalID instance with matching document & external id.
    :rtype: esdoc_api.models.DocumentExternalID

    """
    q = session.query(DocumentExternalID)
    q = q.filter(DocumentExternalID.Project_ID==project_id)
    q = q.filter(DocumentExternalID.Document_ID==document_id)
    q = q.filter(DocumentExternalID.ExternalID==external_id)

    return q.first()


def get_document_external_ids(document_id, project_id=None):
    """Returns a DocumentExternalID instance with matching document & external id.

    :param document_id: ID of a Document instance.
    :type document_id: int

    :param project_id: ID of a Project instance.
    :type project_id: int or None

    :param external_id: An external ID.
    :type external_id: str

    :returns: First DocumentExternalID instance with matching document & external id.
    :rtype: esdoc_api.models.DocumentExternalID

    """
    q = session.query(DocumentExternalID)
    q = q.filter(DocumentExternalID.Document_ID==document_id)
    if project_id is not None:
        q = q.filter(DocumentExternalID.Project_ID==project_id)

    return q.all()


def get_document_summary(document_id, language_id):
    """Returns a DocumentSummary instance with matching document & language.

    :param document_id: ID of a Document instance.
    :type document_id: int

    :param language_id: ID of a DocumentLanguage instance.
    :type language_id: int

    :returns: First DocumentSummary instance with matching document & language.
    :rtype: esdoc_api.models.DocumentSummary

    """
    q = session.query(DocumentSummary)
    q = q.filter(DocumentSummary.Document_ID==document_id)
    q = q.filter(DocumentSummary.Language_ID==language_id)

    return q.first()


def get_document_summaries(project_id, type, version, language_id):
    """Returns a list of DocumentSummary instance with matching criteria.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param type: Document type.
    :type type: str

    :param version: Document version (latest | all).
    :type version: str

    :param language_id: ID of a DocumentLanguage instance.
    :type language_id: int

    :returns: First DocumentSummary instance with matching document & language.
    :rtype: esdoc_api.models.DocumentSummary

    """
    q = session.query(DocumentSummary).join(Document)
    q = q.filter(Document.Project_ID==project_id)
    q = q.filter(DocumentSummary.Language_ID==language_id)
    if type != models.DOCUMENT_TYPE_ALL:
        q = q.filter(Document.Type==type.upper())
    if version.upper() == models.DOCUMENT_VERSION_LATEST:
        q = q.filter(Document.IsLatest==True)

    q = q.limit(session.QUERY_LIMIT)
    
    return sort(DocumentSummary, q.all())


def get_doc_ontology(name, version=None):
    """Returns a DocumentOntology instance with matching name & version.

    :param name: Ontology name.
    :type name: str

    :param version: Ontology version.
    :type version: str

    :returns: First DocumentOntology instance with matching name & version.
    :rtype: esdoc_api.models.DocumentOntology

    """
    q = session.query(DocumentOntology)
    if version is not None:
        name += '.'
        name += str(version)
    q = q.filter(DocumentOntology.Name==name.lower())

    return q.first()


def get_doc_language(code=pyesdoc.ESDOC_DEFAULT_LANGUAGE):
    """Returns a DocumentLanguage instance by it's code.

    :param type: A supported entity type.
    :type type: class

    :param name: Entity code.
    :type name: str

    :returns: First DocumentLanguage with matching code.
    :rtype: esdoc_api.models.DocumentLanguage

    """
    return get_by_facet(DocumentLanguage, DocumentLanguage.Code==code.lower())


def get_ingest_endpoint(url):
    """Returns an IngestEndpoint instance by it's url.

    :param url: URL of an IngestEndpoint instance to be retrieved.
    :type url: str

    :returns: First IngestEndpoint instance with matching url.
    :rtype: esdoc_api.models.IngestEndpoint

    """
    return get_by_facet(IngestEndpoint, IngestEndpoint.IngestURL==url)


def get_ingest_endpoints():
    """Returns a list of active IngestEndpoint instances.

    :returns: List of active IngestEndpoint instances.
    :rtype: list

    """
    q = session.query(IngestEndpoint)
    q = q.filter(IngestEndpoint.IsActive==True)
    q = q.order_by(IngestEndpoint.Priority.desc())

    return q.all()

    #return get_active(IngestEndpoint)


def get_ingest_url(url):
    """Returns an IngestURL instance by it's url.

    :param url: URL of an IngestURL instance to be retrieved.
    :type url: str

    :returns: First IngestURL instance with matching url.
    :rtype: esdoc_api.models.IngestURL

    """
    return get_by_facet(IngestURL, IngestURL.URL==url)


def get_facet(type_id, key):
    """Returns a Facet instance by it's type & key.

    :param type: ID of FacetType instance.
    :type type: int

    :param key: Facet key, e.g. IPSL-CM5A-MR.
    :type key: str

    :returns: First Facet instance with matching type & key.
    :rtype: esdoc_api.models.Facet

    """
    q = session.query(Facet)
    q = q.filter(Facet.Type_ID==type_id)
    q = q.filter(Facet.Key==key[:2047])

    return q.first()


def get_facet_relation(relation_type_id, from_facet_id, to_facet_id):
    """Returns a FacetRelation instance by it's type & key.

    :param relation_type_id: ID of a FacetRelationType instance.
    :type relation_type_id: int

    :param from_facet_id: ID of a Facet instance.
    :type from_facet_id: int

    :param to_facet_id: ID of a Facet instance.
    :type to_facet_id: int

    :returns: First FacetRelation instance with matching relation type, from / to facets.
    :rtype: esdoc_api.models.FacetRelation

    """
    q = session.query(FacetRelation)
    q = q.filter(FacetRelation.Type_ID==relation_type_id)
    q = q.filter(FacetRelation.From_ID==from_facet_id)
    q = q.filter(FacetRelation.To_ID==to_facet_id)

    return q.first()


def get_facet_relation_types():
    """Returns list of facet relation types.

    :returns: A list of facet relation types.
    :rtype: list

    """
    return [get_by_name(FacetRelationType, i) for i in models.FACET_RELATION_TYPES]


def get_facet_types():
    """Returns list of facet types.

    :returns: A list of facet types.
    :rtype: list

    """
    return [get_by_name(FacetType, i) for i in models.FACET_TYPES]


def get_doc_representation(document_id, ontology_id, encoding_id, language_id):
    """Returns a DocumentRepresentation instance with matching ontology, encoding and language.

    :param document_id: ID of a Document instance.
    :type document_id: int

    :param ontology_id: ID of a DocumentOntology instance.
    :type ontology_id: int

    :param encoding_id: ID of a DocumentEncoding instance.
    :type encoding_id: int

    :param language_id: ID of a DocumentLanguage instance.
    :type language_id: int

    :returns: A document representation instance.
    :rtype: esdoc_api.models.document_representation.DocumentRepresentation

    """
    q = session.query(DocumentRepresentation)
    q = q.filter(DocumentRepresentation.Document_ID==document_id)
    q = q.filter(DocumentRepresentation.Ontology_ID==ontology_id)
    q = q.filter(DocumentRepresentation.Encoding_ID==encoding_id)
    q = q.filter(DocumentRepresentation.Language_ID==language_id)

    return q.first()


def _delete_document_relation(document_id, type):
    """Deletes all document relations of passed type.

    :param document_id: ID of a Document instance.
    :type document_id: int

    :param type: Type of relation.
    :type type: class

    """
    delete_by_facet(type, type.Document_ID==document_id)


def delete_document_representations(document_id):
    """Deletes all document representations.

    :param document_id: ID of a Document instance.
    :type document_id: int

    """
    _delete_document_relation(document_id, DocumentRepresentation)


def delete_document_summaries(document_id):
    """Deletes a list of DocumentSummary instances filtered by their Document ID.

    :param document_id: ID of a Document instance.
    :type document_id: int

    """
    _delete_document_relation(document_id, DocumentSummary)


def delete_document_sub_documents(document_id):
    """Deletes a list of DocumentSubDocument instances filtered by their Document ID.

    :param document_id: ID of a Document instance.
    :type document_id: int

    """
    delete_by_facet(DocumentSubDocument, DocumentSubDocument.SubDocument_ID==document_id)
    delete_by_facet(DocumentSubDocument, DocumentSubDocument.Document_ID==document_id)


def delete_document_external_ids(document_id):
    """Deletes a list of DocumentExternalID instances filtered by their Document ID.

    :param document_id: ID of a Document instance.
    :type document_id: int

    """
    _delete_document_relation(document_id, DocumentExternalID)
    

def delete_document_drs(document_id):
    """Deletes a list of DocumentDRS instances filtered by their Document ID.

    :param document_id: ID of a Document instance.
    :type document_id: int

    """
    _delete_document_relation(document_id, DocumentDRS)


def delete_document(document_id):
    """Deletes a document.

    :param document_id: ID of a Document instance.
    :type document_id: int

    """    
    delete_document_drs(document_id)
    delete_document_external_ids(document_id)
    delete_document_representations(document_id)
    delete_document_sub_documents(document_id)
    delete_document_summaries(document_id)    
    delete_by_id(Document, document_id)
    

def delete_all_documents():
    """Deletes all documents.

    """
    delete_by_type(Document, delete_document)


def get_project_document_type_counts(project_id):
    """Returns list of counts over a project's document types.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :returns: List of counts over a project's document types.
    :rtype: list
    
    """
    q = session.query(sa.func.count(Document.Type), Document.Type)
    q = q.filter(Document.Project_ID==project_id)
    q = q.group_by(Document.Type)
    
    return q.all()


def get_project_document_language_counts(project_id):
    """Returns list of counts over a project's document languages.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :returns: List of counts over a project's language types.
    :rtype: list

    """
    q = session.query(sa.func.count(DocumentSummary.Language_ID), DocumentSummary.Language_ID)
    q = q.join(Document)
    q = q.filter(Document.Project_ID==project_id)
    q = q.group_by(DocumentSummary.Language_ID)

    return q.all()



def get_doc_descriptions(project_id, language_id, type):
    """Returns document descriptions.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param language_id: ID of a DocumentLanguage instance.
    :type language_id: int
    
    :param type: Type of Document instance.
    :type type: str

    :returns: Dictionary of project document desciptions.
    :rtype: dict

    """
    q = session.query(Document.Name, DocumentSummary.Description)
    q = q.join(DocumentSummary)
    q = q.filter(Document.IsLatest==True)
    q = q.filter(Document.Project_ID==project_id)
    q = q.filter(Document.Type==type)
    q = q.filter(DocumentSummary.Language_ID==language_id)

    return q.all()
