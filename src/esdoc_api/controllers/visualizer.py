"""
.. module:: esdoc_api.controllers.visualizer
   :platform: Unix, Windows
   :synopsis: Encapsulates visualizer setup operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest

from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.lib.db.facets.utils import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *
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


def _get_v1_setup_data():
    """Loads setup data for the v1 visualizer.

    """
    return {
        'facetSet' : {
            'component' : get_facet_values(MODEL_COMPONENT),
            'model' : get_facet_values(MODEL),
        },
        'relationSet' : {
            'componentToComponent' : get_facet_relations(COMPONENT_2_COMPONENT),
            'modelToComponent' : get_facet_relations(MODEL_2_COMPONENT)
        }
    }


# Set of visualizers and their associated setup function pointers.
_visualizers = {
    'v1' : _get_v1_setup_data
}


class VisualizerController(BaseAPIController):
    """CIM repository visualizer controller.

    """
    @property
    def validate_doc_request_info(self):
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


    def __validate_visualizer_type(self, code):
        """Validates visualizer type.

        :param code: The visualizer type, e.g. v1.
        :type code: str

        """
        # 406 if unsupported.
        if code not in _visualizers:
            msg = 'Visualizer ({0}) is unsupported.'.format(code)
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, msg)


    @rest.restrict('GET')
    @jsonify
    def get_setup_data(self, project_code, visualizer_type):
        """Returns visualizer setup data.

        :param project_code: The project code, e.g. CMIP5.
        :param visualizer_type: The visualizer type, e.g. v1.
        :type project_code: str
        :type visualizer_type: str

        :returns: Visualizer setup data.
        :rtype: dict

        """
        # Format params.
        project_code = project_code.upper()
        visualizer_type = visualizer_type.lower()

        # Validate params.
        self.__validate_project_code(project_code)
        self.__validate_visualizer_type(visualizer_type)

        # Return setup data.
        return {
            'visualizer' : visualizer_type,
            'project' : project_code,
            'data' : _visualizers[visualizer_type]()
        }
        