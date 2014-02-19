"""
.. module:: esdoc_api.comparator.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates set of documentation comparison functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import json
import os

import esdoc_api.models as models
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt


def _get_c1_setup_data(project_id):
    """Loads setup data for the c1 comparator."""
    return {
        'facetSet' : {
            'component' : utils.get_facets(project_id, models.MODEL_COMPONENT),
            'model' : utils.get_facets(project_id, models.MODEL),
            'property' : utils.get_facets(project_id, models.MODEL_COMPONENT_PROPERTY),
            'value' : utils.get_facets(project_id, models.MODEL_COMPONENT_PROPERTY_VALUE),
        },
        'relationSet' : {
            'componentToComponent' : utils.get_facet_relations(project_id, models.COMPONENT_2_COMPONENT),
            'componentToProperty' : utils.get_facet_relations(project_id, models.COMPONENT_2_PROPERTY),
            'modelToComponent' : utils.get_facet_relations(project_id, models.MODEL_2_COMPONENT),
            'modelToProperty' : utils.get_facet_relations(project_id, models.MODEL_2_PROPERTY),
            'modelToValue' : utils.get_facet_relations(project_id, models.MODEL_2_VALUE),
            'propertyToProperty' : utils.get_facet_relations(project_id, models.PROPERTY_2_PROPERTY),
            'propertyToValue' : utils.get_facet_relations(project_id, models.PROPERTY_2_VALUE),
        },
        'joinSet' : {
            'modelToPropertyAndValue' : [],
        }
    }

# Set of comparators and their associated setup function pointers.
_comparators = {
    'c1' : {
        'title' : 'Model Component Properties',
        'setup' : _get_c1_setup_data
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


def get_setup_data(project_code, comparator_type):
    """Returns comparator setup data.

    :param project_code: The project code, e.g. CMIP5.
    :type project_code: str

    :param comparator_type: The comparator code, e.g. c1.
    :type comparator_type: str

    :returns: Comparator setup data.
    :rtype: dict

    """
    # Defensive programming.
    # ... unspecified project code.
    if project_code is None:
        msg = 'Project code is unspecified.'
        rt.throw(msg)

    # ... unspecified comparator type.
    if comparator_type is None:
        msg = 'Comparator is unspecified.'
        rt.throw(msg)

    # ... unsupported comparator type.
    if comparator_type.lower() not in _comparators:
        msg = 'Comparator ({0}) is unsupported.'.format(comparator_type)
        rt.throw(msg)

    # Format input params.
    project_code = project_code.upper()
    comparator_type = comparator_type.lower()

    # Load project.
    project = _get_project(project_code)

    # Return setup data.
    return {
        'comparator' : comparator_type,
        'title' : _comparators[comparator_type]['title'],
        'project' : project_code,
        'data' : _comparators[comparator_type]['setup'](project.ID)
    }


def write_comparator_json(project_code, comparator_type):
    """Writes comparator setup data (in both json and jsonp format) to the file system.

    :param project_code: The project code, e.g. CMIP5.
    :type project_code: str
    
    :param comparator_type: The comparator code, e.g. c1.
    :type comparator_type: str

    """
    # Get data.
    data = get_setup_data(project_code, comparator_type)

    # Set file path.
    path = os.path.dirname(os.path.abspath(__file__))
    path = path.replace("lib/api", "static/json")
    path += "/compare.setup.{0}.{1}.json".format(project_code.lower(),
                                                 comparator_type.lower())

    # Write json file.
    with open(path, 'w') as f:
        json.dump(data, f, encoding="ISO-8859-1")

    # Write jsonp file.
    with open(path + 'p', 'w') as f:
        f.write('onESDOC_JSONPLoad(')
        json.dump(data, f, encoding="ISO-8859-1")
        f.write(');')
    