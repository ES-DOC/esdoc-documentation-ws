"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session
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

    for row in get_rows(_data):
        # Cache.
        if row[0] + row[1] not in ontologies:
            ontologies[row[0] + row[1]] = dao.get_document_ontology(row[0], row[1])

        # Create.
        i = models.DocumentType()
        i.Ontology_ID = ontologies[row[0] + row[1]].ID
        i.Package = row[2].upper()
        i.Name = row[3].upper()
        i.ShortName = row[4].upper()
        i.DisplayName = row[5]

        # Persist.
        session.insert(i)
