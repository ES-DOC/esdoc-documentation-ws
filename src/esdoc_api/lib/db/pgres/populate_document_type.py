"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.lib.db.pgres.utils import get_rows
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_SCHEMAS
from esdoc_api.models.entities.document_schema import DocumentSchema
from esdoc_api.models.entities.document_type import DocumentType


# Module exports.
__all__ = ['populate_document_type']


__compute_nodes = u'''1.5 | quality | cIM_Quality | quality | Quality
1.5 | data | dataObject | data | Data
1.5 | activity | ensemble | ensemble | Ensemble
1.5 | grids | gridSpec | grid | Grid Spec
1.5 | software | modelComponent | model | Model
1.5 | activity | numericalExperiment | experiment | Experiment
1.5 | shared | platform | platform | Platform
1.5 | activity | simulationRun| simulation | Simulation
1.5 | activity | simulationComposite| simulations | Simulations'''


def populate_document_type():
    """Populates collection of cim document schema types.

    Keyword Arguments:
    session - db sesssion.
    """
    schemas = {}

    for row in get_rows(__compute_nodes):
        # Cache.
        if row[0] not in schemas:
            schemas[row[0]] = DocumentSchema.retrieve(row[0])

        # Create.
        dst = DocumentType()
        dst.Schema = schemas[row[0]]
        dst.Package = row[1].upper()
        dst.Name = row[2].upper()
        dst.ShortName = row[3].upper()
        dst.DisplayName = row[4]


