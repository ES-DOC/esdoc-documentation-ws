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

from esdoc_api.lib.db.facets.utils import (
    get_facet_values,
    get_facet_relations
    )
from esdoc_api.models.entities.facet_type import (
    MODEL,
    MODEL_COMPONENT,
    MODEL_COMPONENT_PROPERTY,
    MODEL_COMPONENT_PROPERTY_VALUE
    )
from esdoc_api.models.entities.facet_relation_type import (
    MODEL_2_EXPERIMENT,
    MODEL_2_INSTITUTE,
    MODEL_2_COMPONENT,
    MODEL_2_PROPERTY,
    MODEL_2_VALUE,
    COMPONENT_2_COMPONENT,
    COMPONENT_2_PROPERTY,
    PROPERTY_2_PROPERTY,
    PROPERTY_2_VALUE
    )
from esdoc_api.lib.utils.exception import ESDOCAPIException



def _get_c1_setup_data():
    """Loads setup data for the c1 comparator.

    """
    return {
        'facetSet' : {
            'component' : get_facet_values(MODEL_COMPONENT),
            'model' : get_facet_values(MODEL),
            'property' : get_facet_values(MODEL_COMPONENT_PROPERTY),
            'value' : get_facet_values(MODEL_COMPONENT_PROPERTY_VALUE),
        },
        'relationSet' : {
            'componentToComponent' : get_facet_relations(COMPONENT_2_COMPONENT),
            'componentToProperty' : get_facet_relations(COMPONENT_2_PROPERTY),
            'modelToComponent' : get_facet_relations(MODEL_2_COMPONENT),
            'modelToProperty' : get_facet_relations(MODEL_2_PROPERTY),
            'modelToValue' : get_facet_relations(MODEL_2_VALUE),
            'propertyToProperty' : get_facet_relations(PROPERTY_2_PROPERTY),
            'propertyToValue' : get_facet_relations(PROPERTY_2_VALUE),
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
        raise ESDOCAPIException("Project code must be specified.")

    # Error if not found.
    if c.get_project(code) is None:
        msg = 'Project code ({0}) is unsupported.'
        msg = msg.format(code)
        raise ESDOCAPIException(msg)


def get_setup_data(project_code, comparator_type):
    """Returns comparator setup data.

    :param project_code: The project code, e.g. CMIP5.
    :type project_code: str

    :param comparator_type: The comparator code, e.g. c1.
    :type comparator_type: str

    :returns: Comparator setup data.
    :rtype: dict

    """
    # Validate input params.
    # ... unspecified project code.
    if project_code is None:
        msg = 'Project code is unspecified.'
        raise ESDOCAPIException(msg)

    # ... unspecified comparator type.
    if comparator_type is None:
        msg = 'Comparator is unspecified.'
        raise ESDOCAPIException(msg)

    # ... unsupported comparator type.
    if comparator_type.lower() not in _comparators:
        msg = 'Comparator ({0}) is unsupported.'.format(comparator_type)
        raise ESDOCAPIException(msg)

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


def write_comparator_jsonp(project_code, comparator_type):
    """Writes comparator setup data (in jsonp format) to the file systems.

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



if __name__ == "__main__":
    from esdoc_api.lib.db.pgres.connect import *
    
    write_comparator_jsonp("cmip5", "c1")
    