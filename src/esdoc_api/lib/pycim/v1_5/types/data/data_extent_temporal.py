"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.505242.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.data.data_extent_time_interval import DataExtentTimeInterval



# Module exports.
__all__ = ['DataExtentTemporal']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.505242$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class DataExtentTemporal(object):
    """A concrete class within the cim v1.5 type system.

    A data object temporal extent represents the temporal coverage associated with a data object.
    """

    def __init__(self):
        """Constructor"""
        super(DataExtentTemporal, self).__init__()
        self.begin = datetime.date(1900, 1, 1)       # type = datetime.date
        self.end = datetime.date(1900, 1, 1)         # type = datetime.date
        self.time_interval = None                    # type = data.DataExtentTimeInterval


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
        append(d, 'begin', self.begin, False, True, False)
        append(d, 'end', self.end, False, True, False)
        append(d, 'time_interval', self.time_interval, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

