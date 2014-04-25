"""
.. module:: esdoc_api.lib.repo.init.populate_facet_relation_type.py
   :platform: Unix
   :synopsis: Populates collection of supported facet relation types.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.session as session
import esdoc_api.models as models



def populate_facet_relation_type():
    """Populates collection of supported facet types.

    """
    for name in models.FACET_RELATION_TYPES:
        # Create.
        i = models.FacetRelationType()
        i.Name = name

        # Persist.
        session.insert(i)
