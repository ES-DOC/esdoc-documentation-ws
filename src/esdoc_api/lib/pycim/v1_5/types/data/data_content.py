"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.502644.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.data_source import DataSource
from esdoc_api.lib.pycim.v1_5.types.data.data_topic import DataTopic



# Module exports.
__all__ = ['DataContent']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.502644$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class DataContent(DataSource):
    """A concrete class within the cim v1.5 type system.

    The contents of the data object; like ISO: MD_ContentInformation.
    """

    def __init__(self):
        """Constructor"""
        super(DataContent, self).__init__()
        self.aggregation = str()                     # type = str
        self.frequency = str()                       # type = str
        self.topic = None                            # type = data.DataTopic


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
        d = dict(super(DataContent, self).as_dict())
        append(d, 'aggregation', self.aggregation, False, True, False)
        append(d, 'frequency', self.frequency, False, True, False)
        append(d, 'topic', self.topic, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

