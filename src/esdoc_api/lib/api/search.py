"""
.. module:: esdoc_api.lib.search_engine_results.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search engine execution functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.lib.api.search_d1 as d1
import esdoc_api.lib.api.search_d2 as d2
import esdoc_api.lib.api.search_d3 as d3
import esdoc_api.lib.api.search_d4 as d4
import esdoc_api.lib.api.search_ds1 as ds1
import esdoc_api.lib.api.search_se1 as se1
import esdoc_api.db.models as models
import esdoc_api.db.cache as cache
import esdoc_api.lib.utils.runtime as rt



# Set of supported search types.
_search_types = {
    'documentByDRS' : d1,
    'documentByExternalID' : d2,
    'documentByID' : d3,
    'documentByName' : d4,
    'documentSummaryByName' : ds1,
    'se1' : se1,
}


def _validate_criteria(criteria):
    """Validates search input criteria.

    :param criteria: Search input criteria.
    :type criteria: dict

    """
    rt.assert_var('criteria', criteria, dict)
    rt.assert_params(criteria, [
        ('project', cache.get_names(models.Project))
    ])


def _parse_criteria(criteria):
    """Parses search input criteria.

    :param criteria: Search input criteria.
    :type criteria: dict

    """
    for target in ['project']:
        if target in criteria:
            criteria[target] = str(criteria[target]).lower()


def get_setup_data(type, project):
    """Loads search engine setup data.

    :param type: The Search type, e.g. se1.
    :type type: str

    :param project: The associated project code.
    :type project: str

    :returns: Search setup data.
    :rtype: dict

    """
    return {
        'engine' : type,
        'project' : project,
        'data' : _search_types[type].get_setup(project)
    }


def get_results_data(type, criteria):
    """Loads search engine results data.

    :param type: The Search type, e.g. se1.
    :type type: str

    :param criteria: Search input criteria.
    :type criteria: dict

    :returns: Search results data.
    :rtype: list

    """
    # Parse and validate input params.
    se = _search_types[type]
    for f in [_parse_criteria, se.parse_criteria]:
        f(criteria)
    for v in [_validate_criteria, se.validate_criteria]:
        v(criteria)

    # Return results data.
    data = {
        'engine' : type,
        'timestamp' : criteria['timestamp'],
        'results' : se.get_results(criteria),
        'project' : criteria['project'],
    }

    # Allow search engine to return subdata.
    if hasattr(se, 'set_results_subdata'):
        se.set_results_subdata(data, criteria)

    rt.log("Search returned :: " + str(len(data['results'])) + " results")

    return data
