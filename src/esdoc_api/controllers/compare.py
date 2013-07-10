"""
.. module:: esdoc_api.controllers.comparator
   :platform: Unix, Windows
   :synopsis: Encapsulates comparator setup and differencing operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import json

from pylons.decorators import rest

from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.api.comparator_setup import get_setup_data



# Set of comparators and their associated setup function pointers.
_comparators = [
    'c1'
]


class ComparatorController(BaseAPIController):
    """CIM repository comparator controller.

    """
    def __validate_project_code(self, code):
        """Validates project code in readiness for subsequent actions.

        :param code: The project code, e.g. CMIP5.
        :type code: str

        """
        # 400 if unspecified.
        if code is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Project code is unspecified')

        # 406 if unsupported.
        if c.get_project(code.upper()) is None:
            msg = 'Project code ({0}) is unsupported.'
            msg = msg.format(code.upper())
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, msg)


    def __validate_comparator_type(self, type):
        """Validates comparator type.

        :param type: The comparator type, e.g. c1.
        :type type: str

        """
        # 400 if unspecified.
        if type is None:
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Comparator type is unspecified')

        # 406 if unsupported.
        if type.lower() not in _comparators:
            msg = 'Comparator ({0}) is unsupported.'.format(type.lower())
            abort(HTTP_RESPONSE_NOT_ACCEPTABLE, msg)


    @rest.restrict('GET')
    @jsonify
    def get_setup_data(self, project_code, comparator_type):
        """Returns document matched by project, type, version and language.

        :param project_code: The project code, e.g. CMIP5.
        :type project_code: str

        :param comparator_type: The comparator code, e.g. c1.
        :type comparator_type: str

        :returns: Comparator setup data.
        :rtype: dict

        """
        # Validate params.
        self.__validate_project_code(project_code)
        self.__validate_comparator_type(comparator_type)

        # Return setup data.
        return get_setup_data(project_code, comparator_type)


