"""Populates collection of supported facet types.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session



def populate_facet():
    """Populates collection of supported facets.

    """
    for institute in dao.get_all(models.Institute):
        # Create.
        i = models.Facet()
        i.Key = institute.Name.upper()
        i.Type_ID = models.ID_OF_FACET_INSTITUTE
        i.Value = institute.Name

        # Persist.
        session.insert(i)

