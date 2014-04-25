"""
.. module:: prodiguer_shared_tests.test_utils.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Set of test utility functions.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""
# Module imports.
from sqlalchemy.exc import IntegrityError

from nose.tools import nottest

import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.pyesdoc.ontologies.cim.v1.types as cim_v1
from esdoc_api_test.utils_core import *


def decode_pyesdoc_obj(ontology_name, ontology_version, xml_file, expected_type):
    """Decodes a test xml file & performs basic assertions.

    :param ontology_name: Ontology name.
    :type ontology_name: str

    :param ontology_version: Ontology version.
    :type ontology_version: str

    :param xml_file: Name of xml file to be opened.
    :type xml_file: str

    :param expected_type: Type that the decoded instance should be.
    :type expected_type: class

    :returns: Decoded object.
    :rtype: object

    """
    # Open xml file.
    xml = get_test_file(ontology_name, ontology_version, xml_file)

    # Decode pyesdoc object.
    pyesdoc_obj = pyesdoc.decode(xml, ontology_name, ontology_version, 'xml')

    # Perform basic assertions.
    assert pyesdoc_obj is not None
    assert isinstance(pyesdoc_obj, expected_type)

    return pyesdoc_obj


def get_test_pyesdoc_doc():
    """Returns a pyesdoc object for test purposes.

    """
    doc = decode_pyesdoc_obj('cim', '1', 'software.model_component.xml', cim_v1.ModelComponent)
    assert_object(doc, cim_v1.ModelComponent)

    return doc


def get_test_document(id=None, version=None, project=None):
    """Factory method to instantiate and return a test Document instance.

    :returns: A test Document instance.
    :rtype: esdoc_api.models.Document

    """
    project = project if project is not None else get_test_model(models.Project)
    endpoint = get_test_model(models.IngestEndpoint)
    doc = get_test_pyesdoc_doc()
    doc.meta.id = get_uuid() if id is None else id
    doc.meta.version = 1 if version is None else version
        
    return utils.create_doc(doc, project, endpoint)


def _hydrate_docs_document(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Project_ID = get_test_model_id(models.Project)
    instance.Institute_ID = get_test_model_id(models.Institute)
    instance.IngestEndpoint_ID = get_test_model_id(models.IngestEndpoint)
    instance.Type = get_string(255).upper()
    instance.Name = get_string(255)
    instance.UID = get_string(63)
    instance.Version = get_int()
    instance.HasChildren = get_boolean()
    instance.IsChild = get_boolean()
    instance.IsLatest = get_boolean()
    instance.IsIndexed = get_boolean()
    instance.IngestDate =  get_date()


def _hydrate_docs_document_drs(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Project_ID = get_test_model_id(models.Project)
    instance.Document_ID = get_test_model_id(models.Document)
    instance.Key_01 = get_string(63).upper()
    instance.Key_02 = get_string(63).upper()
    instance.Key_03 = get_string(63).upper()
    instance.Key_04 = get_string(63).upper()
    instance.Key_05 = get_string(63).upper()
    instance.Key_06 = get_string(63).upper()
    instance.Key_07 = get_string(63).upper()
    instance.Key_08 = get_string(63).upper()
    instance.reset_path()


def _hydrate_docs_document_external_id(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Project_ID = get_test_model_id(models.Project)
    instance.Document_ID = get_test_model_id(models.Document)
    instance.ExternalID = get_string(255).upper()


def _hydrate_docs_document_representation(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Document_ID = get_test_model_id(models.Document)
    instance.Ontology_ID = get_test_model_id(models.DocumentOntology)
    instance.Encoding_ID = get_test_model_id(models.DocumentEncoding)
    instance.Language_ID = get_test_model_id(models.DocumentLanguage)
    instance.Representation = get_string(63)


def _hydrate_docs_document_sub_document(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Document_ID = get_test_model_id(models.Document)
    instance.SubDocument_ID = get_test_model_id(models.Document)


def _hydrate_docs_document_summary(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Document_ID = get_test_model_id(models.Document)
    instance.Language_ID = get_test_model_id(models.DocumentLanguage)
    instance.Description = get_string(1023)
    instance.ShortName = get_string(1023)
    instance.LongName = get_string(1023)
    instance.Field_01 = get_string(1023)
    instance.Field_02 = get_string(1023)
    instance.Field_03 = get_string(1023)
    instance.Field_04 = get_string(1023)
    instance.Field_05 = get_string(1023)
    instance.Field_06 = get_string(1023)
    instance.Field_07 = get_string(1023)
    instance.Field_08 = get_string(1023)


def _hydrate_facets_facet(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Type_ID = get_test_model_id(models.FacetType)
    instance.Key = get_string(2047)
    instance.KeyForSort = get_string(2047)
    instance.Value = get_string(2047)
    instance.ValueForDisplay = get_string(2047)
    instance.URL = get_string(2047)


def _hydrate_facets_facet_relation(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Type_ID = get_test_model_id(models.FacetRelationType)
    instance.From_ID = get_test_model_id(models.Facet)
    instance.To_ID = get_test_model_id(models.Facet)


def _hydrate_facets_facet_relation_type(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Name = get_string(127)


def _hydrate_facets_facet_type(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Name = get_string(127)
    instance.ValueType = models.FACET_VALUE_TYPE_STRING


def _hydrate_ingest_endpoint(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Institute_ID = get_test_model_id(models.Institute)
    instance.Priority =  get_int()
    instance.Description =  get_string(63)
    instance.MetadataSource =  get_string(63)
    instance.IngestorType =  get_string(15)
    instance.ContactName =  get_string(128)
    instance.ContactEmail =  get_string(128)
    instance.ContactTelephone =  get_string(128)
    instance.IsActive = get_boolean()
    instance.IngestURL =  get_string(512)


def _hydrate_ingest_history(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Endpoint_ID = get_test_model_id(models.IngestEndpoint)
    instance.State_ID = get_test_model_id(models.IngestState)
    instance.StartDateTime =  get_date()
    instance.EndDateTime =  get_date()
    instance.Count = get_int()
    instance.TimeInMS = get_int()
    instance.ErrorMessage = get_string(1024)


def _hydrate_ingest_url(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.URL = get_string(1023)


def _hydrate_vocab_document_encoding(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Encoding = get_string(15)


def _hydrate_vocab_document_language(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Code = get_string(2)
    instance.Name = get_string(127)


def _hydrate_vocab_document_ontology(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Name = get_string(63)
    instance.Version = get_string(31)


def _hydrate_vocab_document_type(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Ontology_ID = get_test_model_id(models.DocumentOntology)
    instance.Key = get_string(255)
    instance.DisplayName = get_string(63)


def _hydrate_vocab_ingest_state(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Name =  get_string(16)
    instance.Description =  get_string(128)
    instance.Code =  get_int()


def _hydrate_vocab_institute(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Name =  get_string(16)
    instance.Synonym =  get_string(16)
    instance.LongName =  get_string(512)
    instance.CountryCode = get_string(2)
    instance.URL =  get_string(256)


def _hydrate_vocab_project(instance):
    """Hydrates a test instance.

    :param instance: Instance being hydrated.
    :type instance: subclass of prodiguer_shared.models.Entity

    """
    instance.Name =  get_string(16)
    instance.Description =  get_string(1023)
    instance.URL =  get_string(1023)


# Set of supported instance hydrators.
_hydrators = {
    # ... docs models
    models.Document : _hydrate_docs_document,
    models.DocumentDRS : _hydrate_docs_document_drs,
    models.DocumentExternalID : _hydrate_docs_document_external_id,
    models.DocumentRepresentation : _hydrate_docs_document_representation,
    models.DocumentSubDocument : _hydrate_docs_document_sub_document,
    models.DocumentSummary : _hydrate_docs_document_summary,
    # ... facets models
    models.Facet : _hydrate_facets_facet,
    models.FacetRelation : _hydrate_facets_facet_relation,
    models.FacetRelationType : _hydrate_facets_facet_relation_type,
    models.FacetType : _hydrate_facets_facet_type,
    # ... ingest models
    models.IngestEndpoint : _hydrate_ingest_endpoint,
    models.IngestHistory : _hydrate_ingest_history,
    models.IngestURL : _hydrate_ingest_url,
    # ... vocab models
    models.DocumentEncoding : _hydrate_vocab_document_encoding,
    models.DocumentLanguage : _hydrate_vocab_document_language,
    models.DocumentOntology : _hydrate_vocab_document_ontology,
    models.DocumentType : _hydrate_vocab_document_type,
    models.IngestState : _hydrate_vocab_ingest_state,
    models.Institute : _hydrate_vocab_institute,
    models.Project : _hydrate_vocab_project
}


# Test entity instance cache used in rollback scenarios.
_instance_cache = []


def delete_test_models():
    """Deletes all previously created entities.

    """
    # Delete in reverse order of creation.
    #_instance_cache.reverse()
    while len(_instance_cache) > 0:
        try:
            session.delete(_instance_cache.pop())
        # TODO this should not be required
        except IntegrityError:
            session.rollback()
    

@nottest
def get_test_model(type):
    """Creates & returns an entity for testing purposes.

    :param type: Type of entity being tested.
    :type type: class
    
    """
    # Create, cache, hydrate, add to session.
    instance = type()
    _hydrators[type](instance)
    _instance_cache.append(instance)
    session.insert(instance)
    
    return instance


@nottest
def get_test_model_id(type):
    """Creates & returns an entity for testing purposes.

    :param type: Type of entity being tested.
    :type type: class
    
    """
    return get_test_model(type).ID


def assert_model_creation(type):
    """Performs set of entity creation tests.

    :param type: Type of entity being tested.
    :type type: class

    """
    # Create instance directly.
    x = type()
    assert_object(x, type)
    assert_object(x, Entity)

    # Create instance via factory.
    y = get_test_model(type)
    assert_object(y, type)
    assert_object(y, Entity)

    # Reset context.
    delete_test_models()


def assert_model_conversion(type):
    """Performs set of entity conversion tests.

    :param type: Type of entity being tested.
    :type type: class

    """
    # Create instance via factory.
    x = get_test_model(type)
    assert_object(x, type)

    # Convert to string.
    assert models.EntityConvertor.to_string(x) is not None

    # Convert to dictionary.
    assert models.EntityConvertor.to_dict(x) is not None

    # Convert to json.
    assert models.EntityConvertor.to_json(x) is not None

    # Reset context.
    delete_test_models()


def assert_model_persistence(type):
    """Performs set of entity persistence tests.

    :param type: Type of entity being tested.
    :type type: class

    """
    # Cache current count.
    count = dao.get_count(type)

    # Create instance via factory.
    get_test_model(type)

    # Reassert counts.
    assert_int(dao.get_count(type), count + 1)

    # Delete & reassert count.
    delete_test_models()
    assert_int(dao.get_count(type), count)
