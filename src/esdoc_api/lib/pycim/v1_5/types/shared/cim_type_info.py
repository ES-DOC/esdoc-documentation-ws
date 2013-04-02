"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.532973.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.



# Module exports.
__all__ = ['CimTypeInfo']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.532973$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class CimTypeInfo(object):
    """A concrete class within the cim v1.5 type system.

    Encapsulates cim type information.
    """

    def __init__(self):
        """Constructor"""
        super(CimTypeInfo, self).__init__()
        self.package = str()                         # type = str
        self.schema = str()                          # type = str
        self.type = str()                            # type = str
        self.type_display_name = str()               # type = str


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
        append(d, 'package', self.package, False, True, False)
        append(d, 'schema', self.schema, False, True, False)
        append(d, 'type', self.type, False, True, False)
        append(d, 'type_display_name', self.type_display_name, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

