"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.utils.cim_v1 as cim_v1
from esdoc_api.lib.utils.string import get_rows



_data = u'''cim | 1 | quality | cIM_Quality | quality | Quality
cim | 1 | data | dataObject | data | Data
cim | 1 | activity | ensemble | ensemble | Ensemble
cim | 1 | grids | gridSpec | grid | Grid Spec
cim | 1 | software | modelComponent | model | Model
cim | 1 | software | statisticalModelComponent | statistical model | Statistical Model
cim | 1 | activity | numericalExperiment | experiment | Experiment
cim | 1 | shared | platform | platform | Platform
cim | 1 | activity | simulationRun| simulation | Simulation
cim | 1 | activity | simulationComposite| simulations | Simulations'''


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
            ontologies[o + v] = dao.get_document_ontology(o, v)

        # Create.
        i = models.DocumentType()
        i.Ontology_ID = ontologies[o + v].ID
        i.Key = type_key
        i.DisplayName = cim_v1.DISPLAY_NAMES[type_key]

        # Persist.
        session.insert(i)
