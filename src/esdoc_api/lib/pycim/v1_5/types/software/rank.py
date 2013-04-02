"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.562743.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.



# Module exports.
__all__ = ['Rank']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.562743$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Rank(object):
    """A concrete class within the cim v1.5 type system.

    
    """

    def __init__(self):
        """Constructor"""
        super(Rank, self).__init__()
        self.increment = int()                       # type = int
        self.max = int()                             # type = int
        self.min = int()                             # type = int
        self.value = int()                           # type = int


    def as_dict(self):
        """Gets dictionary representation of self used to create other representations such as json, xml ...etc.

        """
        def append(d, key, value, is_iterative, is_primitive, is_enum):
            if value is None:
                if is_iterative:
                    value = []
            elif is_primitive == False and is_enum == False:
                if is_iterative:
                    value = map(lambda i : i.as_dict(), value)
                else:
                    value = value.as_dict()
            d[key] = value

        # Populate a deep dictionary.
        d = dict()
        append(d, 'increment', self.increment, False, True, False)
        append(d, 'max', self.max, False, True, False)
        append(d, 'min', self.min, False, True, False)
        append(d, 'value', self.value, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

