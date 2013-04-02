"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.521578.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.grids.coordinate_list import CoordinateList
from esdoc_api.lib.pycim.v1_5.types.grids.grid_property import GridProperty



# Module exports.
__all__ = ['VerticalCoordinateList']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.521578$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class VerticalCoordinateList(CoordinateList):
    """A concrete class within the cim v1.5 type system.

    There are some specific attributes that are associated with vertical coordinates.
    """

    def __init__(self):
        """Constructor"""
        super(VerticalCoordinateList, self).__init__()
        self.form = str()                            # type = str
        self.properties = []                         # type = grids.GridProperty
        self.type = str()                            # type = str


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
        d = dict(super(VerticalCoordinateList, self).as_dict())
        append(d, 'form', self.form, False, True, False)
        append(d, 'properties', self.properties, True, False, False)
        append(d, 'type', self.type, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

