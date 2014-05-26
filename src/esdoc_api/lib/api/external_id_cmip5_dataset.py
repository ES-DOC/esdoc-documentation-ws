"""
.. module:: esdoc_api.lib.ajax.external_id_cmip5_dataset.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates CMIP5 dataset id handling.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.lib.api.external_id_utils import (
    concat_ds,
    set_cmip5_id
    )
import esdoc_api.db.dao as dao
import esdoc_api.lib.utils.cim_v1 as cim_v1


def parse(id):
    """Performs a parse over a cmip5 dataset id.

    :param id: CMIP5 dataset id.
    :type id: str

    """
    class CMIP5DatasetID(object):
        def __init__(self, id):
            set_cmip5_id(id, self)

    return CMIP5DatasetID(id)


def do_query(project, id):
    """Query handler for returning documents by cmip5 dataset id.

    :param project: CMIP5 project identifier.
    :type project: esdoc_api.db.models.Project

    :param id: CMIP5 dataset identifier
    :type id: CMIP5DatasetID

    :returns: List of found documents.
    :rtype: list

    """
    result = []

    # Source 1 : From DRS keys.
    get = dao.get_document_by_drs_keys
    result = concat_ds(result, get(project.ID,
                                   id.institute,
                                   id.model,
                                   id.experiment,
                                   id.ensemble))

    # Source 2 : From model, experiment (if DRS returned nothing).
    if len(result) == 0:
        get = dao.get_document_by_name
        result = concat_ds(result, get(project.ID,
                                       cim_v1.TYPE_KEY_MODEL_COMPONENT,
                                       id.model))

        result = concat_ds(result, get(project.ID,
                                       cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT,
                                       id.experiment))

    # Source 3 : From dataset ID.
    get = dao.get_documents_by_external_id
    result =  concat_ds(result, get(project.ID, id.id))

    return result


def is_valid(id):
    """Validates a cmip5 dataset id.

    :param id: A cmip5 dataset id.
    :type id: str

    """
    return False if len(id.split('.')) < 9 else True
