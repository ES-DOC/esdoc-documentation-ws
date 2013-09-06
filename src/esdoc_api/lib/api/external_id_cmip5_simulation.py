"""
.. module:: esdoc_api.lib.ajax.external_id_cmip5_simulation.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates CMIP5 simulation id handling.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.lib.api.external_id_utils import concat_ds
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.utils.cim_v1 as cim_v1


def parse(id):
    """Performs a parse over a cmip5 simulation id.

    :param id: CMIP5 simulation id.
    :type id: str

    """
    class CMIP5SimulationID(object):
        def __init__(self, id):
            self.id = id
            self.simulation_id = id
            id = id.split('_')
            if len(id) > 0:
                self.institute = id[0]
            if len(id) > 1:
                self.model = id[1]
            if len(id) > 2:
                self.experiment = id[2]
            if len(id) > 3:
                self.ensemble = id[3]
            if len(id) > 4:
                self.start_year = id[4]

    return CMIP5SimulationID(id)


def do_query(project, id):
    """Query handler for returning documents by cmip5 simulation id.

    :param project: CMIP5 project identifier.
    :type project: esdoc_api.models.Project

    :param id: CMIP5 simulation identifier
    :type id: CMIP5SimulationID

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
                                   id.ensemble,
                                   id.start_year))

    # Source 2 : From model, experiment (if DRS returned nothing).
    if len(result) == 0:
        get = dao.get_document_by_name
        result = concat_ds(result, get(project.ID,
                                       cim_v1.TYPE_KEY_MODEL_COMPONENT,
                                       id.model))

        result = concat_ds(result, get(project.ID,
                                       cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT,
                                       id.experiment))

    # Source 3 : From simulation ID.
    get = dao.get_documents_by_external_id
    return concat_ds(result, get(project.ID, id.simulation_id))


def is_valid(id):
    """Validates a cmip5 simulation id.

    :param id: A cmip5 simulation id.
    :type id: str

    """
    return False if len(id.split('_')) < 5 else True
