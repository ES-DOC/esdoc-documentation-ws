"""Populates collection of supported facet types.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.facet_relation_type import FacetRelationType
from esdoc_api.models.entities.facet_relation_type import FACET_RELATIONS



def populate_facet_relation_type():
    """Populates collection of supported facet types.

    """
    for name in FACET_RELATIONS:
        frt = FacetRelationType()
        frt.Name = name

