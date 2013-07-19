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
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt


def _get_c1_setup_data():
    """Loads setup data for the c1 comparator.

    """
    return {
        'facetSet' : {
            'component' : utils.get_facets(models.MODEL_COMPONENT),
            'model' : utils.get_facets(models.MODEL),
            'property' : utils.get_facets(models.MODEL_COMPONENT_PROPERTY),
            'value' : utils.get_facets(models.MODEL_COMPONENT_PROPERTY_VALUE),
        },
        'relationSet' : {
            'componentToComponent' : utils.get_facet_relations(models.COMPONENT_2_COMPONENT),
            'componentToProperty' : utils.get_facet_relations(models.COMPONENT_2_PROPERTY),
            'modelToComponent' : utils.get_facet_relations(models.MODEL_2_COMPONENT),
            'modelToProperty' : utils.get_facet_relations(models.MODEL_2_PROPERTY),
            'modelToValue' : utils.get_facet_relations(models.MODEL_2_VALUE),
            'propertyToProperty' : utils.get_facet_relations(models.PROPERTY_2_PROPERTY),
            'propertyToValue' : utils.get_facet_relations(models.PROPERTY_2_VALUE),
        }
    }

# Set of comparators and their associated setup function pointers.
_comparators = {
    'c1' : {
        'title' : 'Model Component Properties',
        'setup' : _get_c1_setup_data
    }
}


def _validate_project_code(code):
    """Validates project code in readiness for subsequent actions.

    :param code: The project code, e.g. CMIP5.
    :type code: str

    """
    # Error if unspecified.
    if code is None:
        raise rt.ESDOC_API_Error("Project code must be specified.")

    # Error if not found.
    if c.get_project(code) is None:
        msg = 'Project code ({0}) is unsupported.'
        msg = msg.format(code)
        raise rt.ESDOC_API_Error(msg)


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
        raise rt.ESDOC_API_Error(msg)

    # ... unspecified comparator type.
    if comparator_type is None:
        msg = 'Comparator is unspecified.'
        raise rt.ESDOC_API_Error(msg)

    # ... unsupported comparator type.
    if comparator_type.lower() not in _comparators:
        msg = 'Comparator ({0}) is unsupported.'.format(comparator_type)
        raise rt.ESDOC_API_Error(msg)

    # Format input params.
    project_code = project_code.upper()
    comparator_type = comparator_type.lower()

    # Return setup data.
    return {
        'comparator' : comparator_type,
        'title' : _comparators[comparator_type]['title'],
        'project' : project_code,
        'data' : _comparators[comparator_type]['setup']()
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
    path += "/compare.setup.{0}.{1}.json".format(project_code.lower(), comparator_type.lower())

    # Write json file.
    with open(path, 'w') as f:
        json.dump(data, f, encoding="ISO-8859-1")

    # Write jsonp file.
    with open(path + 'p', 'w') as f:
        f.write('onESDOC_JSONPLoad(')
        json.dump(data, f, encoding="ISO-8859-1")
        f.write(');')
    