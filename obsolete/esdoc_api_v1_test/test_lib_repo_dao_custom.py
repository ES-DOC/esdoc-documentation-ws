"""
.. module:: esdoc_api_test.test_repo_dao_2.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: 2nd set of repository dao functional tests - N.B. these tests are against a pre-populated repo.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""

# Module imports.
import esdoc_api.db.dao as dao
import esdoc_api.db.models as models
import esdoc_api_test.utils as tu



def test_get_document_01():
    # Tests retrieiving a Document instance by it's project, UID & version.
    type = models.Document
    instance1 = tu.get_test_model(type)

    instance2 = dao.get_document(instance1.Project_ID,
                                 instance1.UID,
                                 instance1.Version)
    tu.assert_entity(instance1, instance2)


def test_get_document_02():
    # Tests retrieiving latest Document instance by it's project, UID & version.
    type = models.Document
    instance1 = tu.get_test_model(type)

    instance2 = dao.get_document(instance1.Project_ID,
                                 instance1.UID,
                                 models.DOCUMENT_VERSION_LATEST)
    tu.assert_entity(instance1, instance2)


def test_get_document_03():
    # Tests retrieiving latest Document instance by it's project, UID & version.
    type = models.Document
    instance = tu.get_test_model(type)

    collection = dao.get_document(instance.Project_ID,
                                  instance.UID,
                                  models.DOCUMENT_VERSION_ALL)
    tu.assert_iter(collection, 1)


def test_get_document_by_name():
    # Tests retrieiving a Document instance by it's name.
    type = models.Document
    instance1 = tu.get_test_model(type)

    instance2 = dao.get_document_by_name(instance1.Project_ID,
                                         instance1.Type,
                                         instance1.Name,
                                         instance1.Institute_ID,
                                         latest_only=True)
    tu.assert_entity(instance1, instance2)



def test_get_document_by_drs_keys():
    # Tests retrieiving a Document instance by it's drs keys.
    drs = tu.get_test_model(models.DocumentDRS)
    instance1 = dao.get_by_id(models.Document, drs.Document_ID)
    tu.assert_object(instance1, models.Document)
    instance2 = dao.get_document_by_drs_keys(instance1.Project_ID,
                                            drs.Key_01,
                                            drs.Key_02,
                                            drs.Key_03,
                                            drs.Key_04,
                                            drs.Key_05,
                                            drs.Key_06,
                                            drs.Key_07,
                                            drs.Key_08)
    tu.assert_object(instance2, models.Document)
    tu.assert_entity(instance1, instance2)
    

def test_get_documents_by_external_id():
    # Tests retrieiving a list of documents with a matching external ID.    
    external_id = tu.get_test_model(models.DocumentExternalID)
    document = dao.get_by_id(models.Document, external_id.Document_ID)
    tu.assert_object(document, models.Document)
    documents = dao.get_documents_by_external_id(document.Project_ID, external_id.ExternalID)
    tu.assert_iter(documents, length=1, item_type=models.Document)
    tu.assert_entity(document, documents[0])
    


def test_get_document_drs():
    # Tests retrieiving a DocumentDRS instance with matching document & drs path.
    pass


def test_get_document_external_id():
    # Tests retrieiving a DocumentExternalID instance with matching document & external id.
    pass


def test_get_document_external_ids():
    # Tests retrieiving a list of DocumentExternalID instances with matching document & project id.
    pass


def test_get_document_summary():
    # Tests retrieiving a DocumentSummary instance with matching document & language.
    pass


def test_get_doc_ontology():
    # Tests retrieiving a DocumentOntology instance with matching name & version.
    pass


def test_get_doc_language():
    # Tests retrieiving a DocumentLanguage instance by it's code.
    pass


def test_get_ingest_endpoint():
    # Tests retrieiving an IngestEndpoint instance by it's url.
    pass


def test_get_ingest_endpoints():
    # Tests retrieiving a a list of active IngestEndpoint instances.
    pass


def test_get_ingest_url():
    # Tests retrieiving an IngestURL instance by it's url.
    pass


def test_get_facet():
    # Tests retrieiving a Facet instance by it's type & key.
    pass


def test_get_facet_relation():
    # Tests retrieiving a FacetRelation instance by it's type & key.
    pass


def test_get_facet_relation_types():
    # Tests retrieiving a list of FacetRelationType instances.
    pass


def test_get_facet_types():
    # Tests retrieiving a list of FacetType instances.
    pass


def test_delete_document_summaries():
    # Tests deleting a list of DocumentSummary instances filtered by their Document ID.
    pass


def test_delete_document_drs():
    # Tests deleting a list of DocumentDRS instances filtered by their Document ID.
    pass


def test_delete_document():
    # Tests deleting a Document instance.
    pass


def test_delete_all_documents():
    # Tests deleting all Document instances.
    pass
