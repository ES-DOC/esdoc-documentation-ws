"""Populates collection of supported facet types.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.facet_type import FacetType
from esdoc_api.models.entities.facet_type import FACET_VALUE_TYPE_STRING
from esdoc_api.models.entities.facet_type import EXPERIMENT
from esdoc_api.models.entities.facet_type import INSTITUTE
from esdoc_api.models.entities.facet_type import MODEL
from esdoc_api.models.entities.facet_type import MODEL_COMPONENT
from esdoc_api.models.entities.facet_type import MODEL_COMPONENT_PROPERTY
from esdoc_api.models.entities.facet_type import MODEL_COMPONENT_PROPERTY_VALUE



_types = [
    (EXPERIMENT, FACET_VALUE_TYPE_STRING),
    (INSTITUTE, FACET_VALUE_TYPE_STRING),
    (MODEL, FACET_VALUE_TYPE_STRING),
    (MODEL_COMPONENT, FACET_VALUE_TYPE_STRING),
    (MODEL_COMPONENT_PROPERTY, FACET_VALUE_TYPE_STRING),
    (MODEL_COMPONENT_PROPERTY_VALUE, FACET_VALUE_TYPE_STRING)
]


def populate_facet_type():
    """Populates collection of supported facet types.

    """
    for type in _types:
        ft = FacetType()
        ft.Name = type[0]
        ft.ValueType = type[1]

