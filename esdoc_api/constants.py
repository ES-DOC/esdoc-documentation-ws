# -*- coding: utf-8 -*-
"""
.. module:: constants.py
   :platform: Unix
   :synopsis: Constants used across web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Token used to indicate that all document types are in scope.
DOCUMENT_TYPE_ALL = '*'

# Set of document types supported by web-service.
DOCUMENT_TYPES = [
	{
		'display_name': 'Data',
		'is_search_target': False,
		'is_pdf_target': False,
		'key': 'cim.1.data.DataObject'
	},
	{
		'display_name': 'Simulation',
		'is_search_target': True,
		'is_pdf_target': False,
		'key': 'cim.1.misc.DocumentSet'
	},
	{
		'display_name': 'Ensemble',
		'is_search_target': False,
		'is_pdf_target': False,
		'key': 'cim.1.activity.Ensemble'
	},
	{
		'display_name': 'Grid Spec',
		'is_search_target': True,
		'is_pdf_target': False,
		'key': 'cim.1.grids.GridSpec'
	},
	{
		'display_name': 'Model',
		'is_search_target': True,
		'is_pdf_target': False,
		'key': 'cim.1.software.ModelComponent'
	},
	{
		'display_name': 'Experiment',
		'is_search_target': True,
		'is_pdf_target': False,
		'key': 'cim.1.activity.NumericalExperiment'
	},
	{
		'display_name': 'Platform',
		'is_search_target': True,
		'is_pdf_target': False,
		'key': 'cim.1.shared.Platform'
	},
	{
		'display_name': 'Quality',
		'is_search_target': False,
		'is_pdf_target': False,
		'key': 'cim.1.quality.CimQuality'
	},
	{
		'display_name': 'Simulation',
		'is_search_target': False,
		'is_pdf_target': False,
		'key': 'cim.1.activity.SimulationComposite'
	},
	{
		'display_name': 'Simulation',
		'is_search_target': False,
		'is_pdf_target': False,
		'key': 'cim.1.activity.SimulationRun'
	},
	{
		'display_name': 'Statistical Model',
		'is_search_target': False,
		'is_pdf_target': False,
		'key': 'cim.1.activity.StatisticalModelComponent'
	},
	{
		'display_name': 'Experiment',
		'is_search_target': True,
		'is_pdf_target': True,
		'key': 'cim.2.designing.NumericalExperiment'
	}
]

# Set derived values.
for _dt in DOCUMENT_TYPES:
	_dt['ontology'] = "{}.{}".format(_dt['key'].split('.')[0],
									 _dt['key'].split('.')[1])

# Set of supported projects.
PROJECTS = [
	{
		'name': "global",
		'description': "An application placeholder that acts as a null reference",
		'url': None
	},
	{
		'name': "test",
		'description': "A test project plceholder",
		'url': ""
	},
	{
		'name': "CMIP5",
		'description': "Coupled Model Intercomparison Project Phase 5",
		'url': "http://wcrp-climate.org/wgcm-cmip/wgcm-cmip5"
	},
	{
		'name': "CMIP6",
		'description': "Coupled Model Intercomparison Project Phase 6",
		'url': "http://wcrp-climate.org/wgcm-cmip/wgcm-cmip6"
	},
	{
		'name': "CMIP6-DRAFT",
		'description': "Coupled Model Intercomparison Project Phase 6",
		'url': "http://wcrp-climate.org/wgcm-cmip/wgcm-cmip6"
	},
	{
		'name': "DCMIP-2012",
		'description': "2012 Dynamical Core Model Intercomparison Project",
		'url': "http://earthsystemcog.org/projects/dcmip-2012/"
	},
	{
		'name': "QED-2013",
		'description': "2013 Statistical Downscaling Dynamical Core Model Intercomparison Project",
		'url': "http://earthsystemcog.org/projects/downscaling-2013"
	},
	{
		'name': "ESPS",
		'description': "Earth System Prediction Suite",
		'url': "https://www.earthsystemcog.org/projects/esps"
	},
	{
		'name': "DOWNSCALING-METADATA",
		'description': "Downscaling Metadata",
		'url': "https://www.earthsystemcog.org/projects/downscalingmetadata"
	},
	{
		'name': "ES-FDL",
		'description': "Earth System Framework Description Language",
		'url': "https://earthsystemcog.org/projects/es-fdl"
	}
]
