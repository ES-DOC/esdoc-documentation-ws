# -*- coding: utf-8 -*-
"""
.. module:: cmip5_simulation.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates CMIP5 simulation id handling.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db



def _yield_doc_by_name_criteria(parsed_id):
    """Yeilds document by name search criteria."""
    yield 'cim.1.software.modelcomponent', parsed_id.model
    yield 'cim.1.activity.numericalexperiment', parsed_id.experiment


def is_valid(simulation_id):
    """Validates a CMIP5 simulation id.

    :param str simulation_id: A CMIP5 simulation id.

    :returns: A flag indicating whether the id is valid or not.
    :rtype: boolean

    """
    if not simulation_id or not simulation_id.strip():
        return False
    else:
        return False if len(simulation_id.strip().split('_')) < 5 else True


def get_parsed(simulation_id):
    """Returns a parsed a CMIP5 simulation id.

    :param str simulation_id: CMIP5 simulation id.

    :returns: A parsed CMIP5 simulation id.
    :rtype: object

    """
    class SimulationID(object):
        def __init__(self):
            self.id = simulation_id.upper()
            sim_id = self.id.split('_')
            if len(sim_id) > 0:
                self.institute = sim_id[0]
            if len(sim_id) > 1:
                self.model = sim_id[1]
            if len(sim_id) > 2:
                self.experiment = sim_id[2]
            if len(sim_id) > 3:
                self.ensemble = sim_id[3]
            if len(sim_id) > 4:
                self.start_year = sim_id[4]

    return SimulationID()


def do_search(project_id, parsed_id):
    """Executes document search against db.

    :param int project_id: CMIP5 project identifier.
    :param object parsed_id: A parsed CMIP5 dataset identifier

    :returns: A sequence of returned documents.
    :rtype: generator

    """
    def get_by_drs_keys():
        """Searches by DRS keys."""
        yield db.dao.get_document_by_drs_keys(
            project_id,
            parsed_id.institute,
            parsed_id.model,
            parsed_id.experiment,
            parsed_id.ensemble,
            parsed_id.start_year)

    def get_by_name():
        """Searches by name."""
        for doc_type, doc_name in _yield_doc_by_name_criteria(parsed_id):
            doc = db.dao.get_document_by_name(project_id,
                                              doc_type,
                                              doc_name)
            if doc:
                yield doc

    def get_by_dataset_id():
        """Searches by dataset id."""
        return db.dao.get_documents_by_external_id(project_id,
                                                   parsed_id.id)

    for func in (
        get_by_drs_keys,
        get_by_name,
        get_by_dataset_id
        ):
        for doc in (d for d in func() if d):
            yield doc
