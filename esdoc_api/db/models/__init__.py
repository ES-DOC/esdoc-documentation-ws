# -*- coding: utf-8 -*-
"""
.. module:: __init__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Set of database models supported by ES-DOC API.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db.models.utils import Entity
from esdoc_api.db.models.utils import EntityConvertor
from esdoc_api.db.models.utils import metadata
from esdoc_api.db.models.docs import (
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentSubProject,
    DocumentSummary,
    DOCUMENT_VERSIONS,
    DOCUMENT_VERSION_LATEST,
    DOCUMENT_VERSION_ALL
    )
from esdoc_api.db.models.facets import (
    Node,
    NodeField,
    NODE_TYPES,
    NODE_TYPE_INSTITUTE,
    NODE_TYPE_PROJECT,
    NODE_TYPE_EXPERIMENT,
    NODE_TYPE_MODEL,
    NODE_TYPE_MODEL_COMPONENT,
    NODE_TYPE_MODEL_COMPONENT_PROPERTY,
    NODE_TYPE_MODEL_COMPONENT_PROPERTY_VALUE,
    NODE_TYPE_MODEL_PROPERTY,
    NODE_TYPE_MODEL_PROPERTY_VALUE,
    )
from esdoc_api.db.models.vocab import DocumentEncoding
from esdoc_api.db.models.vocab import DocumentType
from esdoc_api.db.models.vocab import DOCUMENT_TYPE_ALL
from esdoc_api.db.models.vocab import Institute
from esdoc_api.db.models.vocab import Project
from esdoc_api.utils import runtime as rt



# Set of supported model domain partiions (maps to db schemas).
PARTITIONS = set([
    'docs',
    'facets',
    'vocab'
    ])

# Set of supported model types - useful for testing scenarios.
SUPPORTED_TYPES = (
    # ... docs
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentSubProject,
    DocumentSummary,
    # ... facets
    Node,
    NodeField,
    # ... vocab
    DocumentEncoding,
    DocumentType,
    Institute,
    Project
)

# Supported cacheable types.
CACHEABLE_TYPES = (
    DocumentEncoding,
    DocumentType,
    Institute,
    Project,
    NodeField,
    )

# Expose entity conversion methods.
to_dict = EntityConvertor.to_dict
to_dict_for_json = EntityConvertor.to_dict_for_json
to_json = EntityConvertor.to_json
to_string = EntityConvertor.to_string


# Runtime support functions.
def assert_type(mtype):
    """Asserts that passed model type is supported.

    :param class type: A supported entity type.

    """

    def get_msg():
        """Returns error message."""
        return "Unsupported model type ({0}).".format(mtype.__class__.__name__)

    rt.assert_iter_item(SUPPORTED_TYPES, mtype, get_msg)


def assert_instance(instance):
    """Asserts that passed model instance is of a supported type.

    :param Entity instance: A model instance being processed.

    """
    assert_type(instance.__class__)


def assert_iter(collection):
    """Asserts that all collection models instances are of a supported type.

    :param iterable collection: A collection of model instance.

    """
    for instance in collection:
        assert_instance(instance)
