"""
.. module:: esdoc_api.lib.repo.init.populate_facet_type.py
   :platform: Unix
   :synopsis: Populates collection of supported facet types.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.session as session
import esdoc_api.models as models



_data = [
    (models.EXPERIMENT, models.FACET_VALUE_TYPE_STRING),
    (models.INSTITUTE, models.FACET_VALUE_TYPE_STRING),
    (models.MODEL, models.FACET_VALUE_TYPE_STRING),
    (models.MODEL_COMPONENT, models.FACET_VALUE_TYPE_STRING),
    (models.MODEL_COMPONENT_PROPERTY, models.FACET_VALUE_TYPE_STRING),
    (models.MODEL_COMPONENT_PROPERTY_VALUE, models.FACET_VALUE_TYPE_STRING)
]


def populate_facet_type():
    """Populates collection of supported facet types.

    """
    for type in _data:
        # Create.
        i = models.FacetType()
        i.Name = type[0]
        i.ValueType = type[1]

        # Persist.
        session.insert(i)
