"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.515026.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.



# Module exports.
__all__ = ['GridExtent']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.515026$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class GridExtent(object):
    """A concrete class within the cim v1.5 type system.

    DataType for recording the geographic extent of a gridMosaic or gridTile.
    """

    def __init__(self):
        """Constructor"""
        super(GridExtent, self).__init__()
        self.maximum_latitude = str()                # type = str
        self.maximum_longitude = str()               # type = str
        self.minimum_latitude = str()                # type = str
        self.minimum_longitude = str()               # type = str
        self.units = str()                           # type = str


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
        append(d, 'maximum_latitude', self.maximum_latitude, False, True, False)
        append(d, 'maximum_longitude', self.maximum_longitude, False, True, False)
        append(d, 'minimum_latitude', self.minimum_latitude, False, True, False)
        append(d, 'minimum_longitude', self.minimum_longitude, False, True, False)
        append(d, 'units', self.units, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

