# -*- coding: utf-8 -*-

"""
.. module:: esdoc_api.visualizer.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates set of documentation visualization functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import json
import os

from pyesdoc.db import (
    cache,
    dao,
    models
    )
import esdoc_api.lib.utils.runtime as rt


# Encoding type.
_JSON_ENCODING = "ISO-8859-1"



def _get_v1_setup_data(project_id):
    """Loads setup data for the v1 visualizer."""
    return {
        'facetSet' : {
            'component' : utils.get_facets(models.MODEL_COMPONENT),
            'model' : utils.get_facets(models.MODEL),
        },
        'relationSet' : {
            'componentToComponent' : utils.get_facet_relations(project_id, models.COMPONENT_2_COMPONENT),
            'modelToComponent' : utils.get_facet_relations(project_id, models.MODEL_2_COMPONENT),
        }
    }

# Set of visualizers and their associated setup function pointers.
_visualizers = {
    'v1' : {
        'title' : 'Model Components',
        'setup' : _get_v1_setup_data
    }
}


def _get_project(code):
    """Loads project."""
    # Error if unspecified.
    if code is None:
        rt.throw("Project code must be specified.")

    # Error if not found.
    project = dao.get_by_name(models.Project, code.upper())
    if project is None:
        msg = 'Project code ({0}) is unsupported.'
        msg = msg.format(code)
        rt.throw(msg)

    return project


def get_setup_data(project_code, visualizer_type):
    """Returns visualizer setup data.

    :param project_code: The project code, e.g. CMIP5.
    :type project_code: str

    :param visualizer_type: The visualizer code, e.g. c1.
    :type visualizer_type: str

    :returns: Visualizer setup data.
    :rtype: dict

    """
    # Defensive programming.
    # ... unspecified project code.
    if project_code is None:
        msg = 'Project code is unspecified.'
        rt.throw(msg)

    # ... unspecified visualizer type.
    if visualizer_type is None:
        msg = 'Visualizer is unspecified.'
        rt.throw(msg)

    # ... unsupported visualizer type.
    if visualizer_type.lower() not in _visualizers:
        msg = 'Visualizer ({0}) is unsupported.'.format(visualizer_type)
        rt.throw(msg)

    # ... format input params.
    project_code = project_code.upper()
    visualizer_type = visualizer_type.lower()        

    # Load project.
    project = _get_project(project_code)

    # Return setup data.
    return {
        'visualizer' : visualizer_type,
        'title' : _visualizers[visualizer_type]['title'],
        'project' : project_code,
        'data' : _visualizers[visualizer_type]['setup'](project.ID)
    }


def write_visualizer_json(project_code, visualizer_type):
    """Writes visualizer setup data (in both json and jsonp format) to the file system.

    :param project_code: The project code, e.g. CMIP5.
    :type project_code: str
    
    :param visualizer_type: The visualizer code, e.g. c1.
    :type visualizer_type: str

    """
    # Get data.
    data = get_setup_data(project_code, visualizer_type)

    # Set file path.
    path = os.path.dirname(os.path.abspath(__file__))
    path = path.replace("lib/api", "static/json")
    path += "/visualize.setup.{0}.{1}.json".format(project_code.lower(),
                                                 visualizer_type.lower())

    # Write json file.
    with open(path, 'w') as f:
        json.dump(data, f, encoding=_JSON_ENCODING)

    # Write jsonp file.
    with open(path + 'p', 'w') as f:
        f.write('onESDOC_JSONPLoad(')
        json.dump(data, f, encoding=_JSON_ENCODING)
        f.write(');')