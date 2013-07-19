"""
.. module:: esdoc_api.controllers.visualizer
   :platform: Unix, Windows
   :synopsis: Encapsulates visualizer setup operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from pylons.decorators import rest

import esdoc_api.models as models
import esdoc_api.lib.repo.utils as utils
from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *


def _get_v1_setup_data():
    """Loads setup data for the v1 visualizer.

    """
    return {
        'facetSet' : {
            'component' : utils.get_facets(models.MODEL_COMPONENT),
            'model' : utils.get_facets(models.MODEL),
        },
        'relationSet' : {
            'componentToComponent' : daoutils.get_facet_relations(models.COMPONENT_2_COMPONENT),
            'modelToComponent' : daoutils.get_facet_relations(models.MODEL_2_COMPONENT)
        }
    }


# Set of visualizers and their associated setup function pointers.
_visualizers = {
    'v1' : _get_v1_setup_data
}


class VisualizerController(BaseAPIController):
    """CIM repository visualizer controller.

    """
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
        