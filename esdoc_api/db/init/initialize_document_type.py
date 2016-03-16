# -*- coding: utf-8 -*-
"""
.. module:: initialize_document_type.py
   :platform: Unix
   :synopsis: Initializes collection of supported document types.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import dao, models, session



# CIM v1 type keys.
_TYPE_KEY_CIM_1_DATA_OBJECT = 'cim.1.data.DataObject'
_TYPE_KEY_CIM_1_DOCUMENT_SET = 'cim.1.misc.DocumentSet'
_TYPE_KEY_CIM_1_ENSEMBLE = 'cim.1.activity.Ensemble'
_TYPE_KEY_CIM_1_GRID_SPEC = 'cim.1.grids.GridSpec'
_TYPE_KEY_CIM_1_MODEL_COMPONENT = 'cim.1.software.ModelComponent'
_TYPE_KEY_CIM_1_NUMERICAL_EXPERIMENT = 'cim.1.activity.NumericalExperiment'
_TYPE_KEY_CIM_1_PLATFORM = 'cim.1.shared.Platform'
_TYPE_KEY_CIM_1_QUALITY = 'cim.1.quality.CimQuality'
_TYPE_KEY_CIM_1_SIMULATION_COMPOSITE = 'cim.1.activity.SimulationComposite'
_TYPE_KEY_CIM_1_SIMULATION_RUN = 'cim.1.activity.SimulationRun'
_TYPE_KEY_CIM_1_STATISTICAL_MODEL_COMPONENT = 'cim.1.software.StatisticalModelComponent'

# CIM v2 type keys.
_TYPE_KEY_CIM_2_NUMERICAL_EXPERIMENT = 'cim.2.designing.NumericalExperiment'

# Active typeset.
_ACTIVE_TYPES = [
    _TYPE_KEY_CIM_1_DATA_OBJECT,
    _TYPE_KEY_CIM_1_DOCUMENT_SET,
    _TYPE_KEY_CIM_1_ENSEMBLE,
    _TYPE_KEY_CIM_1_GRID_SPEC,
    _TYPE_KEY_CIM_1_MODEL_COMPONENT,
    _TYPE_KEY_CIM_1_NUMERICAL_EXPERIMENT,
    _TYPE_KEY_CIM_1_PLATFORM,
    _TYPE_KEY_CIM_1_QUALITY,
    _TYPE_KEY_CIM_1_SIMULATION_COMPOSITE,
    _TYPE_KEY_CIM_1_SIMULATION_RUN,
    _TYPE_KEY_CIM_1_STATISTICAL_MODEL_COMPONENT,

    _TYPE_KEY_CIM_2_NUMERICAL_EXPERIMENT
]

# Search target typeset.
_SEARCH_TYPES = [
    _TYPE_KEY_CIM_1_DOCUMENT_SET,
    _TYPE_KEY_CIM_1_GRID_SPEC,
    _TYPE_KEY_CIM_1_MODEL_COMPONENT,
    _TYPE_KEY_CIM_1_NUMERICAL_EXPERIMENT,
    _TYPE_KEY_CIM_1_PLATFORM,
    _TYPE_KEY_CIM_2_NUMERICAL_EXPERIMENT
]

# PDF target typeset.
_PDF_TYPES = [
    _TYPE_KEY_CIM_2_NUMERICAL_EXPERIMENT
]


# Display names.
_DISPLAY_NAMES = {
    _TYPE_KEY_CIM_1_DATA_OBJECT: "Data",
    _TYPE_KEY_CIM_1_DOCUMENT_SET: "Simulation",
    _TYPE_KEY_CIM_1_ENSEMBLE: "Ensemble",
    _TYPE_KEY_CIM_1_GRID_SPEC: "Grid Spec",
    _TYPE_KEY_CIM_1_MODEL_COMPONENT: "Model",
    _TYPE_KEY_CIM_1_NUMERICAL_EXPERIMENT: "Experiment",
    _TYPE_KEY_CIM_1_PLATFORM: "Platform",
    _TYPE_KEY_CIM_1_QUALITY: "Quailty",
    _TYPE_KEY_CIM_1_SIMULATION_COMPOSITE: "Simulation",
    _TYPE_KEY_CIM_1_SIMULATION_RUN: "Simulation",
    _TYPE_KEY_CIM_1_STATISTICAL_MODEL_COMPONENT: "Statistical Model",
    _TYPE_KEY_CIM_2_NUMERICAL_EXPERIMENT: "Experiment"
}


def execute():
    """Initializes collection of cim document schema types.

    """
    ontologies = {}

    for type_key in _ACTIVE_TYPES:
        # Unpack type info.
        ontology, version, package, typeof = type_key.split(".")
        ontology = ontology + "." + version

        # Cache.
        if ontology not in ontologies:
            ontologies[ontology] = dao.get_doc_ontology(ontology)

        # Create.
        i = models.DocumentType()
        i.Ontology_ID = ontologies[ontology].ID
        i.Key = unicode(type_key)
        i.DisplayName = unicode(_DISPLAY_NAMES[type_key])
        i.SearchTarget = type_key in _SEARCH_TYPES
        i.IsPdfTarget = type_key in _PDF_TYPES

        # Persist.
        session.insert(i)
