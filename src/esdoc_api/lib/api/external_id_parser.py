"""
.. module:: esdoc_api.lib.ajax.external_id_parser
   :platform: Unix, Windows
   :synopsis: Encapsulates parsing of project specific external document id's.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

def _set_cmip5_id(id, instance):
    """Helper function to parse a cmip5 external id.

    :param id: CMIP5 external identifier.
    :param instance: Parsed external id instance.
    :type id: str
    :type instance: CMIP5DatasetID  | CMIP5FileID
    :returns:
    :rtype: 

    """
    id = id.upper()
    drs = id.split('.')
    instance.id = id
    instance.activity = drs[0]
    instance.project = drs[0]
    instance.product = drs[1]
    instance.institute = drs[2]
    instance.model = drs[3]
    instance.experiment = drs[4]
    instance.frequency = drs[5]
    instance.realm = drs[6]
    instance.mip = drs[7]
    instance.ensemble = drs[8]
    instance.version = drs[9]
    instance.dataset_id = '.'.join(drs[0:9])

    return drs


def cmip5_dataset_id_parser(id):
    """Performs a parse over a cmip5 dataset id.

    :param id: CMIP5 dataset id.
    :type id: str
    
    """
    class CMIP5DatasetID(object):
        def __init__(self, id):
            _set_cmip5_id(id, self)

    return CMIP5DatasetID(id)


def cmip5_file_id_parser(id):
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
            print self.period, self.year, self.month, self.day
                    
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
            drs = _set_cmip5_id(id, self)
            
            # Set file attributes.
            self.file_name = drs[10]
            self.file_parts = drs[10].split('_')
            self.file_extension = drs[11]

            # Set temporal coverage.
            self.temporal_coverage = TemporalCoverage()
            if len(self.file_parts) > 0:
                periods = self.file_parts[len(self.file_parts) - 1]
                periods = periods.split('-')
                self.temporal_coverage.set_periods(periods)

    return CMIP5FileID(id)


def cmip5_simulation_id_parser(id):
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


def dcmip2012_dataset_id_parser(id):
    """Performs a parse over a dcmip2012 dataset id.

    :param id: A dcmip2012 dataset id.
    :type id: str

    """
    class DCMIP2012DatasetID(object):
        def __init__(self, id):
            id = id.upper()
            self.id = id
            drs = id.split('.')
            self.project = drs[0]
            self.model = drs[1]

    return DCMIP2012DatasetID(id)


def dcmip2012_file_id_parser(id):
    """Performs a parse over a dcmip2012 file id.

    :param id: A dcmip2012 file id.
    :type id: str

    """
    class DCMIP2012FileID(object):
        def __init__(self, id):
            id = id.upper()
            self.id = id
            drs = id.split('.')
            self.model = drs[0]

    return DCMIP2012FileID(id)
