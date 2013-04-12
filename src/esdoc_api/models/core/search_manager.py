"""Manages a search.

"""

# Module imports.
from esdoc_api.lib.utils.cim_exception import CIMException
from esdoc_api.models.core.search_base import ESDOCSearchBase


# Module exports.
__all__ = [
    'SearchManager'
]



class SearchManager(object):
    """Encapsulates the management of search process.

    """

    def __init__(self, type, params=None):
        """Constructor.

        :param type: Type of search being executed.
        :param params: Search criteria.

        :type type: subclass of models.core.ESDOCSearchBase
        :type params: dict

        """
        # Defensive programming.
        if type is None:
            raise CIMException("Search type is unspecified.")
        if issubclass(type, ESDOCSearchBase) == False:
            raise CIMException("Search type must derive from models.core.ESDOCSearchBase.")

        # Initialise.
        self.handler = type()
        self.results = None
        self.criteria = self.handler.criteria_type()

        # Hydrate criteria.
        if params is not None:
            self.criteria.hydrate(params)


    def execute(self):
        """Executes search.

        """
        self.results = self.handler.do_search(self.criteria)
        




