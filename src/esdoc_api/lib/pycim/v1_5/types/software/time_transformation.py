"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.566251.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.time_mapping_type import TimeMappingType



# Module exports.
__all__ = ['TimeTransformation']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.566251$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class TimeTransformation(object):
    """A concrete class within the cim v1.5 type system.

    The coupling field used in the target at a given time corresponds to a field produced by the source at a previous time. This lag specifies the difference in time.
    """

    def __init__(self):
        """Constructor"""
        super(TimeTransformation, self).__init__()
        self.description = str()                     # type = str
        self.mapping_type = ''                       # type = software.TimeMappingType


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
        append(d, 'description', self.description, False, True, False)
        append(d, 'mapping_type', self.mapping_type, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

