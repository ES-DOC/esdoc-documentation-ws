# -*- coding: utf-8 -*-

"""
.. module:: esdoc_api.lib.search_engine_se1.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search engine 1 - standard search.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from pyesdoc.db import (
    cache,
    dao,
    models
    )
from pyesdoc.utils import convert
import esdoc_api.lib.utils.runtime as rt


def _to_dict(data):
    """Helper function to return data as a json ready dictionary.

    :param data: Data to be converted to a json ready dictionary.
    :type data: Sub-class of models.Entity or list

    """
    return models.to_dict_for_json(data)


def get_setup():
    """Loads search engine setup data.

    :param str project: The associated project code.

    :returns: Search engine setup data.
    :rtype: dict

    """
    return {
        'projects' : _to_dict(dao.get_all(models.Project)),
        'models' : [],
        'experiments' : [],
        'institutes' : _to_dict(dao.get_all(models.Institute)),
        'instituteCounts' : dao.get_project_institute_counts(),
        'documentTypes' : _to_dict(dao.get_all(models.DocumentType)),
        'documentTypeCounts' : dao.get_project_document_type_counts(),
        'documentLanguages' : _to_dict(dao.get_all(models.DocumentLanguage))
    }


def get_results(criteria):
    """Loads search engine results data.

    :param dict criteria: Search engine input criteria.

    :returns: Search engine results data.
    :rtype: list

    """
    # Extract criteria.
    institute_id = None if 'institute' not in criteria else \
                   cache.get_id(models.Institute, criteria['institute'])
    language_id = cache.get_id(models.DocumentLanguage, criteria['documentLanguage'])
    project_id = cache.get_id(models.Project, criteria['project'])
    doc_type = criteria['documentType']
    version = criteria['documentVersion']

    # Retrieve data.
    data = dao.get_document_summaries(
        project_id,
        doc_type,
        version,
        language_id,
        institute_id)

    # Return data transformed to a dictionary.
    return _to_dict(data)


def set_results_subdata(data, criteria):
    """Assigns search results subdata.

    :param dict data: Search data being returned to client.
    :param dict criteria: Search engine input criteria.

    """
    # Extract criteria.
    project_id = cache.get_id(models.Project, criteria['project'])
    doc_type = criteria['documentType']

    # Set total number of project documents as per document type.
    data['total'] = dao.get_document_type_count(project_id, doc_type)


def validate_criteria(criteria):
    """Validates search engine input criteria.

    :param dict criteria: Search engine input criteria.

    """
    # Verify criteria are within controlled vocabs.
    cache.get_names(models.DocumentLanguage)
    rt.assert_params(criteria, [
        ('documentLanguage', cache.get_names(models.DocumentLanguage)),
        ('documentType', cache.get_names(models.DocumentType)),
        ('documentVersion', models.DOCUMENT_VERSIONS)
    ])


def parse_criteria(criteria):
    """Parses search engine input criteria.

    :param dict criteria: Search engine input criteria.

    """
    # Convert to upper case.
    for target in ['documentLanguage', 'documentType']:
        if target in criteria:
            criteria[target] = str(criteria[target]).upper()

    # Convert to lower case.
    for target in ['documentVersion']:
        if target in criteria:
            criteria[target] = str(criteria[target]).lower()

