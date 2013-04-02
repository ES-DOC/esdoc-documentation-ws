"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.503396.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party import ResponsibleParty



# Module exports.
__all__ = ['DataDistribution']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.503396$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class DataDistribution(object):
    """A concrete class within the cim v1.5 type system.

    Describes how a DataObject is distributed.
    """

    def __init__(self):
        """Constructor"""
        super(DataDistribution, self).__init__()
        self.access = str()                          # type = str
        self.fee = str()                             # type = str
        self.format = str()                          # type = str
        self.responsible_party = None                # type = shared.ResponsibleParty


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
        append(d, 'access', self.access, False, True, False)
        append(d, 'fee', self.fee, False, True, False)
        append(d, 'format', self.format, False, True, False)
        append(d, 'responsible_party', self.responsible_party, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

