"""
.. module:: esdoc_api.lib.search_engine_ds1.py
   :copyright: Copyright "Jun 5, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search engine ds1 - document summary by name.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.db.models as models
import esdoc_api.db.dao as dao
import esdoc_api.db.cache as cache
import esdoc_api.lib.utils.runtime as rt



def get_results(criteria):
    """Loads search engine results data.

    :param criteria: Search engine input criteria.
    :type criteria: dict

    :returns: Search engine results data.
    :rtype: list
    
    """
    pass


def validate_criteria(criteria):
    """Validates search engine input criteria.

    :param criteria: Search engine input criteria.
    :type criteria: dict

    """
    rt.assert_params(criteria, [
        ('encoding', cache.get_names(models.DocumentEncoding)),
        ('language', cache.get_names(models.DocumentLanguage)),
        ('ontology', cache.get_names(models.DocumentOntology)),
    ])


def parse_criteria(criteria):
    """Parses search engine input criteria.

    :param criteria: Search engine input criteria.
    :type criteria: dict
    
    """
    for target in ['encoding', 'language', 'ontology']:
        if target in criteria:
            criteria[target] = str(criteria[target]).upper()
    