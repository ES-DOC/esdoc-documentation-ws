"""Base class for all search handlers.

"""

# Module imports.
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

from esdoc_api.models.core.search_context import SearchContext




class ESDOCSearchBase(object):
    """Base class for all search handlers.

    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta


    def __init__(self, limit=2000):
        """Constructor.

        """
        self.limit = limit


    @abstractproperty
    def criteria_type(self):
        """Gets type representing search criteria.

        """
        pass


    @abstractmethod
    def set_query(self, ctx):
        """Sets query used to drive search process.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass


    @abstractmethod
    def set_query_filter(self, ctx):
        """Applies query filters.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass


    def set_query_sort(self, ctx):
        """Applies query sorts.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass


    def set_query_offset(self, ctx):
        """Applies query offset.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        if ctx.q is not None:
            ctx.q = ctx.q.slice(0, self.limit)


    def do_search(self, criteria):
        """Invokes search.

        :param criteria: Search criteria.
        :type ctx: dict

        """
        # Initialise context.
        ctx = SearchContext(criteria)

        # Prepare query for execution.
        self.set_query(ctx)
        self.set_query_filter(ctx)
        self.set_query_sort(ctx)
        self.set_query_offset(ctx)

        # Execute.
        if ctx.q is not None:
            ctx.r = ctx.q.all()
            print 'SEARCH RETURNED :: {0} records'.format(len(ctx.r))

        # Format.
        if len(ctx.r) > 0 and hasattr(self, 'format_results'):
            ctx.r = self.format_results(ctx.r)

        return ctx.r


class ESDOCSearchCriteriaBase(object):
    """Encapsulates behaviours common to all search criteria.

    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta


    def __init__(self):        
        """Constructor.

        """        
        for key in [k for k in self.keys]:
            setattr(self, key, None)


    def __str__(self):
        """Returns string representation.

        :returns: a string representation of the instance.
        :rtype: str

        """        
        result = ''
        for key in [k for k in self.keys]:
            if len(result):
                result += ', '    
            result += "{0} : {1}".format(key, getattr(self, key))
        return result


    @abstractproperty
    def keys(self):
        """Gets list of criteria keys.

        :returns: a list of criteria keys.
        :rtype: string list

        """
        pass


    def hydrate(self, params):
        """Hydrates criteria state from dictionary of parameters.

        :param params: Search criteria parameters.
        :type params: dict   

        """
        for key in [k for k in self.keys if k in params]:
            value = params[key]

            # set value.
            setattr(self, key, value)

            # format value.
            if hasattr(self, 'format_{0}'.format(key)):
                getattr(self, 'format_{0}'.format(key))()

            # set code.
            if hasattr(self, 'codes') and key in self.codes:
                try:
                    int(value)
                except ValueError:
                    value = self.codes[key](value.upper())
                    setattr(self, key, value.ID if value is not None else 0)
              
    