"""
.. module:: esdoc_api.lib.ajax.external_id
   :platform: Unix, Windows
   :synopsis: Encapsulates querying of repository by project specific external id's.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.models import Project
import esdoc_api.lib.api.external_id_cmip5_dataset as cmip5_dataset
import esdoc_api.lib.api.external_id_cmip5_file as cmip5_file
import esdoc_api.lib.api.external_id_cmip5_simulation as cmip5_simulation
import esdoc_api.lib.api.external_id_dcmip2012_dataset as dcmip2012_dataset
import esdoc_api.lib.api.external_id_dcmip2012_file as dcmip2012_file



# Set of supported query handlers keyed by project.
_handlers = {
    'cmip5' : {
        'dataset' : cmip5_dataset,
        'file' : cmip5_file,
        'simulation' : cmip5_simulation
    },
    'dcmip-2012' : {
        'dataset' : dcmip2012_dataset,
        'file' : dcmip2012_file
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

    project_name = project.Name.lower()
    type = type.lower()
    
    if project_name not in _handlers or \
       type not in _handlers[project_name]:
        return None

    return _handlers[project_name][type]
