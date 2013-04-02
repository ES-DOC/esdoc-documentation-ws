"""
.. module:: pyesdoc_api.lib.ajax.external_id_validator
   :platform: Unix, Windows
   :synopsis: Validates incoming document external ids.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""


def _validate_drs(id, min_length, split='.'):
    """Validates a id by checking it's drs conformance.

    :param id: An external identifier.
    :param min_length: The minimum number of individual components that the id must support.
    :param split: Character used to split identifier into constituent components.
    :type id: str
    :type min_length:
    :type split: str

    :returns: True if valid, False otherwise.
    :rtype: bool

    """
    return False if len(id.split(split)) < min_length else True


def cmip5_dataset_id_validator(id):
    """Validates a cmip5 dataset id.

    :param id: A cmip5 dataset id.
    :type id: str
    
    """
    return _validate_drs(id, 10)


def cmip5_file_id_validator(id):
    """Validates a cmip5 file id.

    :param id: A cmip5 file id.
    :type id: str

    """
    return _validate_drs(id, 12)


def cmip5_simulation_id_validator(id):
    """Validates a cmip5 simulation id.

    :param id: A cmip5 simulation id.
    :type id: str

    """
    return _validate_drs(id, 5, split='_')    


def dcmip2012_dataset_id_validator(id):
    """Validates a dcmip2012 dataset id.

    :param id: A dcmip2012 dataset id.
    :type id: str

    """
    return _validate_drs(id, 2)


def dcmip2012_file_id_validator(id):
    """Validates a dcmip2012 file id.

    :param id: A dcmip2012 file id.
    :type id: str

    """
    return _validate_drs(id, 1)
