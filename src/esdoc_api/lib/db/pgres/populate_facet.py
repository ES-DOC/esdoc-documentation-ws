"""Populates collection of supported facet types.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.institute import Institute
from esdoc_api.models.entities.facet import Facet
from esdoc_api.models.entities.facet_type import ID_OF_FACET_INSTITUTE




def populate_facet():
    """Populates collection of supported facets.

    """
    for institute in Institute.get_all():
        f = Facet()
        f.Key = institute.Name.upper()
        f.Type_ID = ID_OF_FACET_INSTITUTE
        f.Value = institute.Name

