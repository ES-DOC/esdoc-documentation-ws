"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.utils.cim_v1 as cim_v1
from esdoc_api.lib.utils.string import get_rows



def populate_document_type():
    """Populates collection of cim document schema types.

    Keyword Arguments:
    session - db sesssion.
    """
    ontologies = {}

    for type_key in cim_v1.ACTIVE_TYPES:
        # Unpack type info.
        o, v, p, t = type_key.split(".")
        
        # Cache.
        if o + v not in ontologies:
            ontologies[o + v] = dao.get_doc_ontology(o, v)

        # Create.
        i = models.DocumentType()
        i.Ontology_ID = ontologies[o + v].ID
        i.Key = type_key
        i.DisplayName = cim_v1.DISPLAY_NAMES[type_key]

        # Persist.
        session.insert(i)

