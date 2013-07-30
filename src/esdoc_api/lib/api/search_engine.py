"""
.. module:: esdoc_api.lib.search_engine_results.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search engine execution functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.lib.api.search_engine_se1 as se1
import esdoc_api.lib.api.search_engine_ds1 as ds1
import esdoc_api.lib.repo.cache as cache
import esdoc_api.lib.utils.runtime as rt



# Set of supported search engines.
_search_engines = {
    'se1' : se1,
    'documentByExternalID' : ds1
}


def _validate_criteria(criteria):
    """Validates search engine input criteria.

    :param criteria: Search engine input criteria.
    :type criteria: dict

    """
    rt.assert_var('criteria', criteria, dict)
    rt.assert_params(criteria, [
        ('project', cache.get('Project'))
    ])


def _parse_criteria(criteria):
    """Parses search engine input criteria.

    :param criteria: Search engine input criteria.
    :type criteria: dict

    """
    for target in ['project']:
        if target in criteria:
            criteria[target] = str(criteria[target]).upper()


def _validate_search_engine_type(type):
    """Validates that a search engine type is supported.

    :param search_engine_type: The Search engine  type, e.g. se1.
    :type search_engine_type: str

    """
    # Unspecified search engine type.
    if type is None:
        msg = 'Search engine is unspecified.'
        rt.throw(msg)

    # Unsupported comparator type.
    if type not in _search_engines:
        msg = 'Search engine ({0}) is unsupported.'.format(type)
        rt.throw(msg)


def get_setup_data(type):
    """Returns comparator setup data.

    :param type: The Search engine type, e.g. se1.
    :type type: str

    :returns: Search engine setup data.
    :rtype: dict

    """
    # Defensive programming.
    _validate_search_engine_type(type)

    # Return setup data.
    se = _search_engines[type]
    return {
        'engine' : type,
        'data' : se.get_setup()
    }


def get_results_data(type, criteria):
    """Returns comparator setup data.

    :param type: The Search engine type, e.g. se1.
    :type type: str

    :param criteria: Search engine input criteria.
    :type criteria: dict

    :returns: Search engine setup data.
    :rtype: dict

    """
    # Defensive programming.
    _validate_search_engine_type(type)

    # Parse and validate input params.
    se = _search_engines[type]
    for f in [_parse_criteria, se.parse_criteria]:
        f(criteria)
    for v in [_validate_criteria, se.validate_criteria]:
        v(criteria)

    # Return setup data.
    return {
        'engine' : type,
        'data' : se.get_results(criteria),
        'project' : criteria['project'],
    }


