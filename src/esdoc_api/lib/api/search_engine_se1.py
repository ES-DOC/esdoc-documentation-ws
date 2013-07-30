"""
.. module:: esdoc_api.lib.search_engine_se1.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search engine 1 - standard search.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.models as models
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.cache as cache
import esdoc_api.lib.utils.runtime as rt



def get_setup():
    """Loads search engine setup data.

    :returns: Search engine setup data.
    :rtype: dict
    
    """
    return {
        'documentTypes' : models.to_dict_for_json(dao.get_all(models.DocumentType)),
        'documentLanguages' : models.to_dict_for_json(dao.get_all(models.DocumentLanguage))
    }


def get_results(criteria):
    """Loads search engine results data.

    :param criteria: Search engine input criteria.
    :type criteria: dict

    :returns: Search engine results data.
    :rtype: list
    
    """
    return models.to_dict_for_json(
        dao.get_document_summaries(cache.get_id('Project', criteria['project']),
                                   criteria['documentType'],
                                   criteria['documentVersion'],
                                   cache.get_id('DocumentLanguage', criteria['documentLanguage'])))


def validate_criteria(criteria):
    """Validates search engine input criteria.

    :param criteria: Search engine input criteria.
    :type criteria: dict

    """
    rt.assert_params(criteria, [
        ('documentLanguage', cache.get('DocumentLanguage')),
        ('documentType', cache.get('DocumentType')),
        ('documentVersion', models.DOCUMENT_VERSIONS)
    ])


def parse_criteria(criteria):
    """Parses search engine input criteria.

    :param criteria: Search engine input criteria.
    :type criteria: dict
    
    """
    for target in ['documentLanguage', 'documentType', 'documentVersion']:
        if target in criteria:
            criteria[target] = str(criteria[target]).upper()

