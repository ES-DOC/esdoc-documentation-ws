# -*- coding: utf-8 -*-
"""
.. module:: cmip5_file.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A CMIP5 file id handler.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import dao
from esdoc_api.utils.external_id.cmip5_utils import set_cmip5_id



def _yield_doc_by_name_criteria(parsed_id):
    """Yeilds document by name search criteria."""
    yield 'cim.1.software.modelcomponent', parsed_id.model
    yield 'cim.1.activity.numericalexperiment', parsed_id.experiment


def is_valid(file_id):
    """Validates a CMIP5 file id.

    :param str file_id: A CMIP5 file id.

    :returns: A flag indicating whether the id is valid or not.
    :rtype: boolean

    """
    if not file_id or not file_id.strip():
        return False
    else:
        return False if len(file_id.strip().split('.')) < 12 else True


def get_parsed(file_id):
    """Returns a parsed a CMIP5 file id.

    :param str file_id: CMIP5 file id.

    :returns: A parsed CMIP5 file id.
    :rtype: object

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


    class FileID(object):
        def __init__(self):
            # Set core attributes.
            set_cmip5_id(file_id, self)

            # Set file specific attributes.
            self.file_name = self.drs[10]
            self.file_parts = self.drs[10].split('_')
            self.file_extension = self.drs[11]

            # Set temporal coverage attributes.
            self.temporal_coverage = TemporalCoverage()
            if len(self.file_parts) > 0:
                periods = self.file_parts[len(self.file_parts) - 1]
                periods = periods.split('-')
                self.temporal_coverage.set_periods(periods)

    return FileID()


def do_search(project, parsed_id):
    """Executes document search against db.

    :param str project: Project code.
    :param object parsed_id: A parsed CMIP5 dataset identifier

    :returns: A sequence of returned documents.
    :rtype: generator

    """
    def get_by_drs_keys():
        """Searches by DRS keys."""
        yield dao.get_document_by_drs_keys(
            project,
            parsed_id.institute,
            parsed_id.model,
            parsed_id.experiment,
            parsed_id.ensemble)

    def get_by_name():
        """Searches by name."""
        for doc_type, doc_name in _yield_doc_by_name_criteria(parsed_id):
            doc = dao.get_document_by_name(project,
                                           doc_type,
                                           doc_name)
            if doc:
                yield doc

    def get_by_dataset_id():
        """Searches by dataset id."""
        return dao.get_documents_by_external_id(project, parsed_id.id)

    for func in (
        get_by_drs_keys,
        get_by_name,
        get_by_dataset_id
        ):
        for doc in (d for d in func() if d):
            yield doc

