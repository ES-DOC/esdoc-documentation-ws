"""
.. module:: handler.py
   :platform: Unix, Windows
   :synopsis: Encapsulates handling of external identifiers.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from . import (
    cmip5_dataset,
    cmip5_file,
    cmip5_simulation,
    dcmip2012_dataset,
    dcmip2012_file
    )



# Set of supported query handlers keyed by project.
_HANDLERS = {
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


def get(project, type_of):
    """Returns a handler for a CIM document external identifier.

    :param str project: A project leveraging the es-doc api.
    :param str type_of: Type of external identifier.

    :returns: Pointer to external id handler module.
    :rtype: Module pointer.

    """
    try:
        return _HANDLERS[project.lower()][type_of.lower()]
    except KeyError:
        return None
