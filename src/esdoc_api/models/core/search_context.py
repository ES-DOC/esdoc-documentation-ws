"""Encapsulates search process contextual information.

"""

# Module exports.
__all__ = [
    'SearchContext'
]



class SearchContext(object):
    """Encapsulates search process contextual information.

    """
    def __init__(self, criteria):
        """Constructor.

        :param criteria: Search criteria.
        :type criteria: A subclass of models.core.ESDOCSearchCriteriaBase

        """
        self.c = criteria
        self.r = []
        self.q = None
        

    def set_join(self, expression):
        """Adds a join expression to query.
        
        :param expression: Join expression being added to query.
        :type expression: sqlalchemy.expression

        """
        if self.q is not None:
            self.q = self.q.join(expression)


    def set_filter(self, expression):
        """Adds a filter expression to query.

        :param expression: Filter expression being added to query.
        :type expression: sqlalchemy.expression

        """
        if self.q is not None:
            self.q = self.q.filter(expression)


    def set_sort(self, expression):
        """Adds a sort expression to query.
        
        :param expression: Sort expression being added to query.
        :type expression: sqlalchemy.expression

        """
        if self.q is not None:
            self.q = self.q.order_by(expression)

