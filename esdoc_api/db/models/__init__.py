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
from esdoc_api.db.models.docs import Document
from esdoc_api.db.models.docs import DocumentDRS
from esdoc_api.db.models.docs import DocumentExternalID
from esdoc_api.db.models.docs import DocumentSubProject
from esdoc_api.db.models.facets import Node
from esdoc_api.db.models.facets import NodeField
from esdoc_api.db.models.facets import NODE_TYPES
from esdoc_api.db.models.facets import NODE_TYPE_INSTITUTE
from esdoc_api.db.models.facets import NODE_TYPE_PROJECT
from esdoc_api.db.models.facets import NODE_TYPE_EXPERIMENT
from esdoc_api.db.models.facets import NODE_TYPE_MODEL
from esdoc_api.db.models.facets import NODE_TYPE_MODEL_COMPONENT
from esdoc_api.db.models.facets import NODE_TYPE_MODEL_COMPONENT_PROPERTY
from esdoc_api.db.models.facets import NODE_TYPE_MODEL_COMPONENT_PROPERTY_VALUE
from esdoc_api.db.models.facets import NODE_TYPE_MODEL_PROPERTY
from esdoc_api.db.models.facets import NODE_TYPE_MODEL_PROPERTY_VALUE
from esdoc_api.utils import runtime as rt



# Set of supported model domain partiions (maps to db schemas).
PARTITIONS = set([
    'docs',
    'facets'
    ])

# Set of supported model types - useful for testing scenarios.
SUPPORTED_TYPES = (
    # ... docs
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentSubProject,
    # ... facets
    Node,
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
