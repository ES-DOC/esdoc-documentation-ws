"""
.. module:: pyesdoc_api.lib.ajax.external_id
   :platform: Unix, Windows
   :synopsis: Encapsulates querying of repository by project specific external id's.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.api.external_id_parser import (
    cmip5_dataset_id_parser,
    cmip5_file_id_parser,
    cmip5_simulation_id_parser,
    dcmip2012_dataset_id_parser,
    dcmip2012_file_id_parser
    )
from esdoc_api.lib.api.external_id_query import (
    cmip5_dataset_id_query,
    cmip5_file_id_query,
    cmip5_simulation_id_query,
    dcmip2012_dataset_id_query,
    dcmip2012_file_id_query
    )
from esdoc_api.lib.api.external_id_validator import (
    cmip5_dataset_id_validator,
    cmip5_file_id_validator,
    cmip5_simulation_id_validator,
    dcmip2012_dataset_id_validator,
    dcmip2012_file_id_validator
    )
from esdoc_api.models.entities.project import Project


class ExternalIDHandler():
    """An external id handler.

    :ivar parse: Pointer to external id parser function.
    :ivar is_valid: Pointer to external id validator function.
    :ivar do_query: Pointer to external id query function.
    
    """

    def __init__(self, parse, is_valid, do_query):
        """Constructor.

        :ivar parse: Pointer to external id parser function.
        :ivar is_valid: Pointer to external id validator function.
        :ivar do_query: Pointer to external id query function.
        :type parse: Function
        :type is_valid: Function
        :type do_query: Function

        """
        self.parse = parse
        self.is_valid = is_valid
        self.do_query = do_query


# Set of supported query handlers keyed by project.
_handlers = {
    'cmip5' : {
        'dataset' : ExternalIDHandler(cmip5_dataset_id_parser, 
                                      cmip5_dataset_id_validator,
                                      cmip5_dataset_id_query),
        'file' : ExternalIDHandler(cmip5_file_id_parser,
                                   cmip5_file_id_validator,
                                   cmip5_file_id_query),
        'simulation' : ExternalIDHandler(cmip5_simulation_id_parser,
                                         cmip5_simulation_id_validator,
                                         cmip5_simulation_id_query)
    },
    'dcmip-2012' : {
        'dataset' : ExternalIDHandler(dcmip2012_dataset_id_parser,
                                      dcmip2012_dataset_id_validator,
                                      dcmip2012_dataset_id_query),
        'file' : ExternalIDHandler(dcmip2012_file_id_parser,
                                   dcmip2012_file_id_validator,
                                   dcmip2012_file_id_query)
    }
}


def get_handler(project, type):
    """Returns a handler for a CIM document external identifier.

    :param project: A project leveraging the es-doc api.
    :param type: Type of external identifier.
    :type project: str
    :type type: str

    """
    # Defensive programming.
    if isinstance(project, Project) == False:
        raise TypeError('project')

    project = project.Name.lower()
    if project not in _handlers:
        return None

    type = type.lower()
    if type not in _handlers[project]:
        return None

    return _handlers[project][type]
