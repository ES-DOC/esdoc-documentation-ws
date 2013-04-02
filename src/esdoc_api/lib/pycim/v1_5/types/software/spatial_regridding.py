"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.563654.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.spatial_regridding_dimension_type import SpatialRegriddingDimensionType
from esdoc_api.lib.pycim.v1_5.types.software.spatial_regridding_property import SpatialRegriddingProperty
from esdoc_api.lib.pycim.v1_5.types.software.spatial_regridding_standard_method_type import SpatialRegriddingStandardMethodType
from esdoc_api.lib.pycim.v1_5.types.software.spatial_regridding_user_method import SpatialRegriddingUserMethod



# Module exports.
__all__ = ['SpatialRegridding']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.563654$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class SpatialRegridding(object):
    """A concrete class within the cim v1.5 type system.

    Characteristics of the scheme used to interpolate a field from one grid (source grid) to another (target grid).  Documents should use either the spatialRegriddingStandardMethod _or_ the spatialRegriddingUserMethod, but not both.
    """

    def __init__(self):
        """Constructor"""
        super(SpatialRegridding, self).__init__()
        self.dimension = ''                          # type = software.SpatialRegriddingDimensionType
        self.properties = []                         # type = software.SpatialRegriddingProperty
        self.standard_method = ''                    # type = software.SpatialRegriddingStandardMethodType
        self.user_method = None                      # type = software.SpatialRegriddingUserMethod


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
        append(d, 'dimension', self.dimension, False, False, True)
        append(d, 'properties', self.properties, True, False, False)
        append(d, 'standard_method', self.standard_method, False, False, True)
        append(d, 'user_method', self.user_method, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

