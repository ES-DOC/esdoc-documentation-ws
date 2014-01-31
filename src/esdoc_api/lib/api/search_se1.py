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


def _to_dict(data):
    """Helper function to return data as a json ready dictionary.

    :param data: Data to be converted to a json ready dictionary.
    :type data: Sub-class of models.Entity or list

    """
    return models.to_dict_for_json(data)


def get_setup(project):
    """Loads search engine setup data.

    :param str project: The associated project code.
    
    :returns: Search engine setup data.
    :rtype: dict
    
    """
    # Return setup data.
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
                   cache.get_id('Institute', criteria['institute'])
    language_id = cache.get_id('DocumentLanguage', criteria['documentLanguage'])
    project_id = cache.get_id('Project', criteria['project'])
    type = criteria['documentType']
    version = criteria['documentVersion']

    print institute_id, language_id, project_id, type, version

    # Retrieve data.
    data = dao.get_document_summaries(
        project_id,
        type,
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
    project_id = cache.get_id('Project', criteria['project'])
    type = criteria['documentType']

    # Set total number of project documents as per document type.
    data['total'] = dao.get_document_type_count(project_id, type)


def validate_criteria(criteria):
    """Validates search engine input criteria.

    :param dict criteria: Search engine input criteria.

    """
    # Verify criteria are within controlled vocabs.
    rt.assert_params(criteria, [
        ('documentLanguage', cache.get('DocumentLanguage')),
        ('documentType', cache.get('DocumentType')),
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
