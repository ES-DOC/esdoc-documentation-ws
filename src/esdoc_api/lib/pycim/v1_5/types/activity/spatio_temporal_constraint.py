"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.501910.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.activity.numerical_requirement import NumericalRequirement
from esdoc_api.lib.pycim.v1_5.types.shared.date_range import DateRange
from esdoc_api.lib.pycim.v1_5.types.activity.resolution_type import ResolutionType



# Module exports.
__all__ = ['SpatioTemporalConstraint']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.501910$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class SpatioTemporalConstraint(NumericalRequirement):
    """A concrete class within the cim v1.5 type system.

    Contains a set of relationship types specific to a simulation document that can be used to describe its genealogy.
    """

    def __init__(self):
        """Constructor"""
        super(SpatioTemporalConstraint, self).__init__()
        self.date_range = None                       # type = shared.DateRange
        self.spatial_resolution = ''                 # type = activity.ResolutionType

        self.requirement_type = str("spatioTemporalConstraint")


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
        d = dict(super(SpatioTemporalConstraint, self).as_dict())
        append(d, 'date_range', self.date_range, False, False, False)
        append(d, 'spatial_resolution', self.spatial_resolution, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

