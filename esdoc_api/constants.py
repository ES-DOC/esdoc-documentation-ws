# -*- coding: utf-8 -*-
"""
.. module:: constants.py
   :platform: Unix
   :synopsis: Constants used across web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Set of document types supported by web-service.
DOCUMENT_TYPES = {
	'cim.1.data.DataObject': {
		'display_name': 'Data',
		'is_search_target': False,
		'is_pdf_target': False
	},
	'cim.1.misc.DocumentSet': {
		'display_name': 'Simulation',
		'is_search_target': True,
		'is_pdf_target': False
	},
	'cim.1.activity.Ensemble': {
		'display_name': 'Ensemble',
		'is_search_target': False,
		'is_pdf_target': False
	},
	'cim.1.grids.GridSpec': {
		'display_name': 'Grid Spec',
		'is_search_target': True,
		'is_pdf_target': False
	},
	'cim.1.software.ModelComponent': {
		'display_name': 'Model',
		'is_search_target': True,
		'is_pdf_target': False
	},
	'cim.1.activity.NumericalExperiment': {
		'display_name': 'Experiment',
		'is_search_target': True,
		'is_pdf_target': False
	},
	'cim.1.shared.Platform': {
		'display_name': 'Platform',
		'is_search_target': True,
		'is_pdf_target': False
	},
	'cim.1.quality.CimQuality': {
		'display_name': 'Quality',
		'is_search_target': False,
		'is_pdf_target': False
	},
	'cim.1.activity.SimulationComposite': {
		'display_name': 'Simulation',
		'is_search_target': False,
		'is_pdf_target': False
	},
	'cim.1.activity.SimulationRun': {
		'display_name': 'Simulation',
		'is_search_target': False,
		'is_pdf_target': False
	},
	'cim.1.activity.StatisticalModelComponent': {
		'display_name': 'Statistical Model',
		'is_search_target': False,
		'is_pdf_target': False
	},
	'cim.2.designing.NumericalExperiment': {
		'display_name': 'Experiment',
		'is_search_target': True,
		'is_pdf_target': True
	},
}

# Set derived values.
for _dt, _value in DOCUMENT_TYPES.items():
	_value['key'] = unicode(_dt)
	_value['ontology'] = "{}.{}".format(_dt.split('.')[0], _dt.split('.')[1])
