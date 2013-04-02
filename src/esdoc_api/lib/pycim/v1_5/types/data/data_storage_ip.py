"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.512958.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.data.data_storage import DataStorage



# Module exports.
__all__ = ['DataStorageIp']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.512958$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class DataStorageIp(DataStorage):
    """A concrete class within the cim v1.5 type system.

    Contains attributes to describe a DataObject stored as a database file.
    """

    def __init__(self):
        """Constructor"""
        super(DataStorageIp, self).__init__()
        self.file_name = str()                       # type = str
        self.host = str()                            # type = str
        self.path = str()                            # type = str
        self.protocol = str()                        # type = str


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
        d = dict(super(DataStorageIp, self).as_dict())
        append(d, 'file_name', self.file_name, False, True, False)
        append(d, 'host', self.host, False, True, False)
        append(d, 'path', self.path, False, True, False)
        append(d, 'protocol', self.protocol, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

