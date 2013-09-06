"""
.. module:: esdoc_api.lib.ajax.external_id_cmip5_file.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates CMIP5 file id handling.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.lib.api.external_id_utils import (
    concat_ds,
    set_cmip5_id
    )
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.utils.cim_v1 as cim_v1



def parse(id):
    """Performs a parse over a cmip5 file id.

    :param id: CMIP5 file id.
    :type id: str

    """
    class TemporalCoveragePeriod(object):
        def __init__(self):
            self.period = None
            self.year = None
            self.month = None
            self.day = None

        def set_period(self, period):
            self.period = period
            if len(period) >= 4:
                self.year = period[0:4]
            if len(period) >= 6:
                self.month = period[4:6]
            if len(period) >= 8:
                self.day = period[6:8]


    class TemporalCoverage(object):
        def __init__(self):
            self.start = TemporalCoveragePeriod()
            self.end = TemporalCoveragePeriod()

        def set_periods(self, periods):
            if len(periods) > 0:
                self.start.set_period(periods[0])
            if len(periods) > 1:
                self.end.set_period(periods[1])


    class CMIP5FileID(object):
        def __init__(self, id):
            # Set dataset atrnibutes.
            set_cmip5_id(id, self)

            # Set file attributes.
            self.file_name = self.drs[10]
            self.file_parts = self.drs[10].split('_')
            self.file_extension = self.drs[11]

            # Set temporal coverage.
            self.temporal_coverage = TemporalCoverage()
            if len(self.file_parts) > 0:
                periods = self.file_parts[len(self.file_parts) - 1]
                periods = periods.split('-')
                self.temporal_coverage.set_periods(periods)

    return CMIP5FileID(id)


def do_query(project, id):
    """Query handler for returning documents by cmip5 file id.

    :param project: CMIP5 project identifier.
    :type project: esdoc_api.models.Project
    
    :param id: CMIP5 file identifier
    :type id: CMIP5FileID

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
    
    return concat_ds(result, get(project.ID, id.dataset_id))


def is_valid(id):
    """Validates a cmip5 file id.

    :param id: A cmip5 file id.
    :type id: str

    """
    return False if len(id.split('.')) < 12 else True
