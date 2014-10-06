"""
.. module:: cmip5_dataset.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: A CMIP5 dataset id handler.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from pyesdoc.db import dao

from .cmip5_utils import set_cmip5_id



def _yield_doc_by_name_criteria(parsed_id):
    """Yeilds document by name search criteria."""
    yield 'cim.1.software.modelcomponent', parsed_id.model
    yield 'cim.1.activity.numericalexperiment', parsed_id.experiment


def is_valid(dataset_id):
    """Validates a CMIP5 dataset id.

    :param str dataset_id: A CMIP5 dataset id.

    :returns: A flag indicating whether the id is valid or not.
    :rtype: boolean

    """
    if not dataset_id or not dataset_id.strip():
        return False
    else:
        return False if len(dataset_id.strip().split('.')) < 9 else True


def get_parsed(dataset_id):
    """Returns a parsed a CMIP5 dataset id.

    :param str dataset_id: CMIP5 dataset id.

    :returns: A parsed CMIP5 dataset id.
    :rtype: object

    """
    class DatasetID(object):
        """A CMIP5 dataset id wrapper."""
        def __init__(self):
            """Constructor."""
            set_cmip5_id(dataset_id, self)


    return DatasetID()


def do_search(project_id, parsed_id):
    """Executes document search against db.

    :param int project_id: CMIP5 project identifier.
    :param object parsed_id: A parsed CMIP5 dataset identifier

    :returns: A sequence of returned documents.
    :rtype: generator

    """
    def _get_by_drs_keys():
        """Searches by DRS keys."""
        yield dao.get_document_by_drs_keys(project_id,
                                           parsed_id.institute,
                                           parsed_id.model,
                                           parsed_id.experiment,
                                           parsed_id.ensemble)

    def _get_by_name():
        """Searches by name."""
        for doc_type, doc_name in _yield_doc_by_name_criteria(parsed_id):
            yield dao.get_document_by_name(project_id,
                                           doc_type,
                                           doc_name)

    def _get_by_dataset_id():
        """Searches by dataset id."""
        return dao.get_documents_by_external_id(project_id, parsed_id.id)

    for func in (
        _get_by_drs_keys,
        _get_by_name,
        _get_by_dataset_id
        ):
        for doc in (d for d in func() if d):
            yield doc
