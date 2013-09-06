"""
.. module:: esdoc_api.models.__init__.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of models supported by ES-DOC API.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.models.utils import (
    Entity,
    EntityConvertor,
    metadata
    )
from esdoc_api.models.docs import (
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentRepresentation,
    DocumentSubDocument,
    DocumentSummary,
    DOCUMENT_VERSIONS,
    DOCUMENT_VERSION_LATEST,
    DOCUMENT_VERSION_ALL
    )
from esdoc_api.models.facets import (
    FACET_VALUE_TYPES,
    FACET_VALUE_TYPE_BOOLEAN,
    FACET_VALUE_TYPE_DATETIME,
    FACET_VALUE_TYPE_INTEGER,
    FACET_VALUE_TYPE_STRING,
    FACET_TYPES,
    EXPERIMENT,
    INSTITUTE,
    MODEL,
    MODEL_COMPONENT,
    MODEL_COMPONENT_PROPERTY,
    MODEL_COMPONENT_PROPERTY_VALUE,
    ID_OF_FACET_EXPERIMENT,
    ID_OF_FACET_INSTITUTE,
    ID_OF_FACET_MODEL,
    ID_OF_FACET_COMPONENT,
    ID_OF_FACET_PROPERTY,
    ID_OF_FACET_VALUE,
    FACET_RELATION_TYPES,
    MODEL_2_EXPERIMENT,
    MODEL_2_INSTITUTE,
    MODEL_2_COMPONENT,
    MODEL_2_PROPERTY,
    MODEL_2_VALUE,
    COMPONENT_2_COMPONENT,
    COMPONENT_2_PROPERTY,
    PROPERTY_2_PROPERTY,
    PROPERTY_2_VALUE,
    ID_OF_FACET_RELATION_FROM_COMPONENT_2_COMPONENT,
    ID_OF_FACET_RELATION_FROM_COMPONENT_2_PROPERTY,
    ID_OF_FACET_RELATION_FROM_MODEL_2_COMPONENT,
    ID_OF_FACET_RELATION_FROM_MODEL_2_EXPERIMENT,
    ID_OF_FACET_RELATION_FROM_MODEL_2_INSTITUTE,
    ID_OF_FACET_RELATION_FROM_MODEL_2_PROPERTY,
    ID_OF_FACET_RELATION_FROM_MODEL_2_VALUE,
    ID_OF_FACET_RELATION_FROM_PROPERTY_2_PROPERTY,
    ID_OF_FACET_RELATION_FROM_PROPERTY_2_VALUE,
    Facet,
    FacetRelation,
    FacetRelationType,
    FacetType
    )
from esdoc_api.models.ingest import (
    IngestEndpoint,
    IngestHistory,
    IngestURL
    )
from esdoc_api.models.vocab import (
    DocumentEncoding,
    DocumentLanguage,
    DocumentOntology,
    DocumentType,
    DOCUMENT_TYPE_ALL,
    INGEST_STATES,
    INGEST_STATE_QUEUED,
    INGEST_STATE_RUNNING,
    INGEST_STATE_SUSPENDED,
    INGEST_STATE_COMPLETE,
    INGEST_STATE_ERROR,
    INGEST_STATE_QUEUED_ID,
    INGEST_STATE_RUNNING_ID,
    INGEST_STATE_SUSPENDED_ID,
    INGEST_STATE_COMPLETE_ID,
    INGEST_STATE_ERROR_ID,
    IngestState,
    Institute,
    Project
)
import esdoc_api.lib.utils.runtime as rt



# Set of supported model types - useful for testing scenarios.
supported_types = (
    # ... docs
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentRepresentation,
    DocumentSubDocument,
    DocumentSummary,
    # ... facets
    Facet,
    FacetRelation,
    FacetRelationType,
    FacetType,
    # ... ingest
    IngestEndpoint,
    IngestHistory,
    IngestURL,
    # ... vocab
    DocumentEncoding,
    DocumentLanguage,
    DocumentOntology,
    DocumentType,
    IngestState,
    Institute,
    Project
)

# Expose entity conversion methods.
to_dict = EntityConvertor.to_dict
to_dict_for_json = EntityConvertor.to_dict_for_json
to_json = EntityConvertor.to_json
to_string = EntityConvertor.to_string


# Runtime support functions.
def assert_type(type):
    """Asserts that passed type is supported.

    :param type: A supported entity type.
    :type type: class

    """
    def get_msg():
        return "Unsupported model type ({0}).".format(type.__class__.__name__)

    rt.assert_iter_item(supported_types, type, get_msg)


def assert_instance(instance):
    """Asserts that passed instance is of a supported type.

    :param instance: An repo model instance being processed.
    :type instance: sub-class of models.Entity

    """
    assert_type(instance.__class__)


def assert_collection(collection):
    """Asserts that all members of the passed colllection are supported types.

    :param collection: A collection of supported entity types.
    :type collection: iterable

    """
    for instance in collection:
        assert_instance(instance)