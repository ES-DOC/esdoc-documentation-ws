"""
.. module:: pyesdoc_api.controllers.comparator
   :platform: Unix, Windows
   :synopsis: Encapsulates comparator setup and differencing operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest

from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.lib.db.facets.utils import *
from esdoc_api.lib.pycim.cim_constants import *
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


class ComparatorController(BaseAPIController):
    """CIM repository comparator controller.

    """
    @property
    def validate_cim_info(self):
        """Gets flag indicating whether cim http request information should be validated or not.
        
        """
        return False
    

    def __validate_project_code(self, code):
        """Validates project code in readiness for subsequent actions.

        :param code: The project code, e.g. CMIP5.
        :type code: str

        """
        # 400 if unspecified.
        if code is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Bad CIM document request')

        # 406 if not found.
        if c.get_project(code) is None:
            msg = 'Project code ({0}) is unsupported.'
            msg = msg.format(code)
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, msg)


    def __validate_comparator_type(self, code):
        """Validates comparator type.

        :param code: The comparator type, e.g. c1.
        :type code: str

        """
        # 406 if unsupported.
        if code not in _comparators:
            msg = 'Comparator ({0}) is unsupported.'.format(code)
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, msg)


    @rest.restrict('GET')
    @jsonify
    @beaker_cache(type='memory', query_args=True, expire=86400)
    def get_setup_data(self, project_code, comparator_type):
        """Returns document matched by project, type, version and language.

        :param project_code: The project code, e.g. CMIP5.
        :param comparator_type: The comparator code, e.g. c1.
        :type project_code: str
        :type comparator_type: str

        :returns: Comparator setup data.
        :rtype: dict

        """
        # Format params.
        project_code = project_code.upper()
        comparator_type = comparator_type.lower()

        # Validate params.
        self.__validate_project_code(project_code)
        self.__validate_comparator_type(comparator_type)

        # Return setup data.
        return {
            'comparator' : comparator_type,
            'title' : _comparators[comparator_type]['title'],
            'project' : project_code,
            'data' : _comparators[comparator_type]['setup']()
        }
